import os
import telebot
import threading
import time
import uuid
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Environment variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_USERNAME = "@speedy_current_affairs_2026"
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

    # Check if the user is a member of the channel
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    if not is_user_in_channel(user_id):
        # If not a member, show button to join channel
        join_button = InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
        keyboard.add(join_button)
        bot.send_message(user_id, f"🚀 Please join our channel first: {CHANNEL_USERNAME}\nThen press /start again.", reply_markup=keyboard)
    else:
        # If already a member, show the GP link button
        if user_id in user_links:
            bot.send_message(user_id, "❌ You have already used your link. Wait for the next update.")
        else:
            if gplink_url:
                unique_link = f"{gplink_url}?token={uuid.uuid4()}"
                user_links[user_id] = (unique_link, time.time())  # Store the link and its creation time
                
                # Button to get the GP link
                gplink_button = InlineKeyboardButton("Get GPLink", url=unique_link)
                keyboard.add(gplink_button)
                
                bot.send_message(user_id, "🎉 You are a member of the channel! Click below to get your unique link.\n\n⏳ This link will expire in 2 minutes.", reply_markup=keyboard)
            else:
                bot.send_message(user_id, "❌ No link is available right now. Please wait for the admin to update.")

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

# Function to run bot polling and Flask app together
def run_bot():
    bot.polling()

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Run both the bot and Flask app in separate threads
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_flask()
