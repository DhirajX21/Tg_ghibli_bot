import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os

# Fetch the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Please set the BOT_TOKEN environment variable.")

bot = telebot.TeleBot(BOT_TOKEN)

# Function to generate Ghibli or Anime images using an API
def generate_image(choice):
    # Placeholder API endpoint (replace with a real image generation API)
    api_url = "https://api.example.com/generate_image"
    payload = {"style": choice}  # "Ghibli" or "Anime"
    
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        return response.content  # Return raw image data
    else:
        raise Exception("Failed to generate image")

# Main menu with Ghibli and Anime options
def main_menu(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Ghibli", callback_data="Ghibli"))
    markup.add(InlineKeyboardButton("Anime", callback_data="Anime"))
    bot.send_message(chat_id, "What type of image would you like to generate?", reply_markup=markup)

# Welcome message and start menu
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Ghibli & Anime Image Bot! 🎨")
    main_menu(message.chat.id)

# Handle Ghibli or Anime selection
@bot.callback_query_handler(func=lambda call: call.data in ["Ghibli", "Anime"])
def handle_choice(call):
    choice = call.data
    try:
        bot.send_message(call.message.chat.id, f"Generating a {choice} image for you... 🎉")
        image_data = generate_image(choice)
        
        # Send the generated image
        bot.send_photo(call.message.chat.id, photo=image_data)
        
        # Show Back to Main Menu button
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Back to Main Menu", callback_data="main_menu"))
        bot.send_message(call.message.chat.id, "Would you like to return to the main menu?", reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error: {e}. Please try again later.")

# Handle Back to Main Menu button
@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def back_to_main_menu(call):
    main_menu(call.message.chat.id)

# Fallback for unrecognized messages
@bot.message_handler(func=lambda msg: True)
def fallback(message):
    bot.reply_to(message, "Please use the buttons to navigate the bot. 😊")

# Keep the bot running
print("Bot is running...!")
bot.infinity_polling()
