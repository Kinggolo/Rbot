import os
import telebot
import threading
import time
import uuid
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # Added as an environment variable
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)
gplink_url = None
user_links = {}

# Flask app for health check
app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

def is_user_in_channel(user_id):
    """Check if user is in the channel"""
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

def delete_expired_links():
    """Periodically check and delete expired links"""
    while True:
        current_time = time.time()
        expired_users = [user_id for user_id, (link, timestamp) in user_links.items() if current_time - timestamp > 120]
        for user_id in expired_users:
            del user_links[user_id]
            bot.send_message(user_id, "⏳ Your link has expired! Request again later.")
        time.sleep(60)

# Start the expiration checker in a separate thread
threading.Thread(target=delete_expired_links, daemon=True).start()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    # Create an inline keyboard with buttons
    keyboard = InlineKeyboardMarkup()
    join_button = InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")
    keyboard.add(join_button)

    if not is_user_in_channel(user_id):
        bot.send_message(user_id, f"🚀 Please join our channel first: {CHANNEL_USERNAME}\nThen press /start again.", reply_markup=keyboard)
        return

    # Check if the user already got a link
    if user_id in user_links:
        bot.send_message(user_id, "❌ You have already used your link. Wait for the next update.")
        return

    # Create the button for "Get PDF Link"
    pdf_button = InlineKeyboardButton("Get PDF Link", callback_data="get_pdf_link")
    keyboard.add(pdf_button)

    if gplink_url:
        unique_link = f"{gplink_url}?token={uuid.uuid4()}"
        user_links[user_id] = (unique_link, time.time())  # Store the link and its creation time
        bot.send_message(user_id, f"🎉 Here is your unique link:\n{unique_link}\n\n⏳ This link will expire in 2 minutes.", reply_markup=keyboard)
    else:
        bot.send_message(user_id, "❌ No link is available right now. Please wait for the admin to update.", reply_markup=keyboard)

@bot.message_handler(commands=['setlink'])
def set_link(message):
    global gplink_url
    if message.chat.id == ADMIN_ID:
        new_link = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
        if new_link:
            gplink_url = new_link
            bot.send_message(ADMIN_ID, f"✅ GPLink updated to: {gplink_url}")
        else:
            bot.send_message(ADMIN_ID, "❌ Please provide a valid link. Example:\n/setlink https://newgplink.com")
    else:
        bot.send_message(message.chat.id, "❌ You are not authorized to use this command.")

@bot.callback_query_handler(func=lambda call: call.data == "get_pdf_link")
def send_pdf_link(call):
    user_id = call.from_user.id

    if user_id in user_links:
        unique_link, timestamp = user_links[user_id]
        bot.send_message(user_id, f"🎉 Your unique link is ready:\n{unique_link}\n\n⏳ This link will expire in 2 minutes.")
    else:
        bot.send_message(user_id, "❌ You need to join the channel first. Please use the 'Join Channel' button and then try again.")

# Function to run bot polling and Flask app together
def run_bot():
    bot.polling()

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Run both the bot and Flask app in separate threads
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_flask()

# ******************************
# For the functionality to restrict the link request to one-time use:
# You can enable this part tomorrow by uncommenting the following code:

# def delete_user_link(user_id):
#     """Delete the user's link after 2 minutes"""
#     time.sleep(120)
#     if user_id in user_links:
#         del user_links[user_id]
#         bot.send_message(user_id, "⏳ Your link has expired! Request again later.")
# 
# threading.Thread(target=delete_user_link, args=(user_id,)).start()

# ******************************
