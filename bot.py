import telebot from telebot import types import requests import os

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN' ADMIN_ID = 7423694517  # Replace with your Telegram user ID BACKEND_URL = 'https://your-backend-url.onrender.com/generate_image'

bot = telebot.TeleBot(API_TOKEN) user_db = set()

@bot.message_handler(commands=['start']) def send_welcome(message): user_db.add(message.from_user.id) photo = open("welcome.jpg", 'rb') if os.path.exists("welcome.jpg") else None caption = "Welcome to Ghibli BOT. This bot helps you turn your pic into a Ghibli image. Send me your pic." bot.send_photo(message.chat.id, photo, caption=caption) if photo else bot.send_message(message.chat.id, caption)

@bot.message_handler(content_types=['photo']) def ask_style(message): file_info = bot.get_file(message.photo[-1].file_id) downloaded_file = requests.get(f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}") with open("input.jpg", 'wb') as f: f.write(downloaded_file.content)

markup = types.InlineKeyboardMarkup()
markup.add(
    types.InlineKeyboardButton("Ghibli", callback_data="ghibli"),
    types.InlineKeyboardButton("Anime", callback_data="anime")
)
bot.send_message(message.chat.id, "Choose a style:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["ghibli", "anime"]) def generate_image(call): files = {'image': open('input.jpg', 'rb')} data = {'style': call.data} try: r = requests.post(BACKEND_URL, files=files, data=data) if r.status_code == 200: with open("output.jpg", 'wb') as out: out.write(r.content) bot.send_photo(call.message.chat.id, photo=open("output.jpg", 'rb')) else: bot.send_message(call.message.chat.id, "Image generation failed.") except Exception as e: bot.send_message(call.message.chat.id, f"Error: {str(e)}")

@bot.message_handler(commands=['admin']) def admin_panel(message): if message.from_user.id == ADMIN_ID: markup = types.ReplyKeyboardMarkup(resize_keyboard=True) markup.add("Send to All", "Show Users", "Update Welcome Message") bot.send_message(message.chat.id, "Admin Panel:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "Show Users" and m.from_user.id == ADMIN_ID) def show_users(message): bot.send_message(message.chat.id, f"Total users: {len(user_db)}\n{list(user_db)}")

@bot.message_handler(func=lambda m: m.text == "Send to All" and m.from_user.id == ADMIN_ID) def ask_broadcast(message): msg = bot.send_message(message.chat.id, "Type the message to broadcast:") bot.register_next_step_handler(msg, broadcast)

def broadcast(message): for uid in user_db: try: bot.send_message(uid, message.text) except: continue bot.send_message(message.chat.id, "Broadcast sent.")

@bot.message_handler(func=lambda m: m.text == "Update Welcome Message" and m.from_user.id == ADMIN_ID) def update_welcome(message): msg = bot.send_message(message.chat.id, "Send new welcome image:") bot.register_next_step_handler(msg, save_welcome_image)

def save_welcome_image(message): if message.content_type == 'photo': file_info = bot.get_file(message.photo[-1].file_id) downloaded_file = requests.get(f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}") with open("welcome.jpg", 'wb') as f: f.write(downloaded_file.content) bot.send_message(message.chat.id, "Welcome image updated.") else: bot.send_message(message.chat.id, "Please send a photo.")

bot.polling()

app.py (Flask Backend + Admin Panel)

from flask import Flask, request, send_file, render_template from PIL import Image, ImageEnhance import io import os

app = Flask(name)

@app.route('/') def admin_home(): return render_template("index.html")

@app.route('/generate_image', methods=['POST']) def generate_image(): if 'image' not in request.files or 'style' not in request.form: return "Missing data", 400

image_file = request.files['image']
style = request.form['style']

image = Image.open(image_file.stream)

if style == "ghibli":
    image = ImageEnhance.Color(image).enhance(2.0)
elif style == "anime":
    image = ImageEnhance.Brightness(image).enhance(1.3)

output = io.BytesIO()
image.save(output, format='JPEG')
output.seek(0)

return send_file(output, mimetype='image/jpeg')

if name == 'main': app.run(host='0.0.0.0', port=10000)

templates/index.html (Admin Dashboard)

Save this file in a folder named "templates"

<!-- templates/index.html --><!DOCTYPE html><html>
<head>
  <title>Ghibli Bot Admin</title>
  <style>
    body { font-family: Arial; background: #f0f0f0; padding: 30px; }
    h1 { color: #333; }
    .card { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
  </style>
</head>
<body>
  <div class="card">
    <h1>Ghibli Bot Admin Panel</h1>
    <p>This is a basic dashboard. You can enhance it with JS + backend later.</p>
  </div>
</body>
</html>requirements.txt

pyTelegramBotAPI Flask Pillow requests

