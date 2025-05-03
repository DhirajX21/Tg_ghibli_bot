## main.py (Telegram Bot with Admin Features)
import telebot
from telebot import types
import requests
import os

BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
ADMIN_ID = 7423694517  # Replace with your Telegram user ID
BACKEND_URL = 'https://tg-ghibli-bot.onrender.com/generate_image'

bot = telebot.TeleBot(BOT_TOKEN)
user_db = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_db.add(message.from_user.id)
    photo = open("welcome.jpg", 'rb') if os.path.exists("welcome.jpg") else None
    caption = "Welcome to Ghibli BOT. This bot helps you turn your pic into a Ghibli image. Send me your pic."
    bot.send_photo(message.chat.id, photo, caption=caption) if photo else bot.send_message(message.chat.id, caption)

@bot.message_handler(content_types=['photo'])
def ask_style(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = requests.get(f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}")
    with open("input.jpg", 'wb') as f:
        f.write(downloaded_file.content)

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Ghibli", callback_data="ghibli"),
        types.InlineKeyboardButton("Anime", callback_data="anime")
    )
    bot.send_message(message.chat.id, "Choose a style:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["ghibli", "anime"])
def generate_image(call):
    files = {'image': open('input.jpg', 'rb')}
    data = {'style': call.data}
    try:
        r = requests.post(BACKEND_URL, files=files, data=data)
        if r.status_code == 200:
            with open("output.jpg", 'wb') as out:
                out.write(r.content)
            bot.send_photo(call.message.chat.id, photo=open("output.jpg", 'rb'))
        else:
            bot.send_message(call.message.chat.id, "Image generation failed.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Send to All", "Show Users", "Update Welcome Message")
        bot.send_message(message.chat.id, "Admin Panel:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Show Users" and m.from_user.id == ADMIN_ID)
def show_users(message):
    bot.send_message(message.chat.id, f"Total users: {len(user_db)}\n{list(user_db)}")

@bot.message_handler(func=lambda m: m.text == "Send to All" and m.from_user.id == ADMIN_ID)
def ask_broadcast(message):
    msg = bot.send_message(message.chat.id, "Type the message to broadcast:")
    bot.register_next_step_handler(msg, broadcast)

def broadcast(message):
    for uid in user_db:
        try:
            bot.send_message(uid, message.text)
        except:
            continue
    bot.send_message(message.chat.id, "Broadcast sent.")

@bot.message_handler(func=lambda m: m.text == "Update Welcome Message" and m.from_user.id == ADMIN_ID)
def update_welcome(message):
    msg = bot.send_message(message.chat.id, "Send new welcome image:")
    bot.register_next_step_handler(msg, save_welcome_image)

def save_welcome_image(message):
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = requests.get(f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}")
        with open("welcome.jpg", 'wb') as f:
            f.write(downloaded_file.content)
        bot.send_message(message.chat.id, "Welcome image updated.")
    else:
        bot.send_message(message.chat.id, "Please send a photo.")

bot.polling()
