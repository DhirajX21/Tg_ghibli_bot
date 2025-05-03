import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os

# Bot token environment variable se fetch karo
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Please set the BOT_TOKEN environment variable.")

bot = telebot.TeleBot(BOT_TOKEN)

# Function to simulate image generation (replace with actual generation logic or APIs)
def generate_image(choice):
    # Dummy images for demo (replace with actual image generation or URLs)
    ghibli_images = [
        "https://via.placeholder.com/400x300.png?text=Ghibli+Image+1",
        "https://via.placeholder.com/400x300.png?text=Ghibli+Image+2",
    ]
    anime_images = [
        "https://via.placeholder.com/400x300.png?text=Anime+Image+1",
        "https://via.placeholder.com/400x300.png?text=Anime+Image+2",
    ]
    return random.choice(ghibli_images if choice == "Ghibli" else anime_images)

# Welcome message and image choice
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Ghibli & Anime Image Bot! 🎨")
    markup = InlineKeyboardMarkup()
    ghibli_button = InlineKeyboardButton("Ghibli", callback_data="Ghibli")
    anime_button = InlineKeyboardButton("Anime", callback_data="Anime")
    markup.add(ghibli_button, anime_button)
    bot.send_message(message.chat.id, "What type of image would you like to generate?", reply_markup=markup)

# Handle button clicks
@bot.callback_query_handler(func=lambda call: call.data in ["Ghibli", "Anime"])
def handle_choice(call):
    choice = call.data
    bot.send_message(call.message.chat.id, f"Generating a {choice} image for you... 🎉")
    image_url = generate_image(choice)
    bot.send_photo(call.message.chat.id, photo=image_url)

# Fallback for unrecognized messages
@bot.message_handler(func=lambda msg: True)
def fallback(message):
    bot.reply_to(message, "Please choose Ghibli or Anime using the buttons. 😊")

# Keep the bot running
print("Bot is running...")
bot.infinity_polling()