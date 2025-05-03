import telebot
import requests
from telebot import types

API_TOKEN = 'YOUR_BOT_TOKEN'
BACKEND_URL = 'https://your-backend-url.onrender.com/generate_image'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Ghibli")
    btn2 = types.KeyboardButton("Anime")
    markup.add(btn1, btn2)
    bot.send_message(
        message.chat.id,
        "Welcome to the Ghibli & Anime Image Bot! What type of image would you like to generate?",
        reply_markup=markup
    )

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file = requests.get(f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}")
    with open("input.jpg", "wb") as f:
        f.write(file.content)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Ghibli", callback_data="ghibli"))
    markup.add(types.InlineKeyboardButton("Anime", callback_data="anime"))
    bot.send_message(message.chat.id, "Select style:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    style = call.data
    files = {'image': open('input.jpg', 'rb')}
    data = {'style': style}
    try:
        response = requests.post(BACKEND_URL, files=files, data=data)
        if response.status_code == 200:
            with open("output.jpg", "wb") as out:
                out.write(response.content)
            bot.send_photo(call.message.chat.id, photo=open("output.jpg", 'rb'))
        else:
            bot.send_message(call.message.chat.id, "Image generation failed.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error: {str(e)}")

bot.polling()
