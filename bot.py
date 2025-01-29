import telebot
import threading
import time
import uuid  # For generating unique tokens

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_USERNAME = "@yourchannel"
ADMIN_ID = 123456789  # Replace with your Telegram ID

bot = telebot.TeleBot(TOKEN)
gplink_url = None  # Admin will set this manually
user_links = {}  # Dictionary to store user-specific links

def is_user_in_channel(user_id):
    """Check if user is in the channel"""
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

def delete_user_link(user_id):
    """Delete the user's link after 2 minutes"""
    time.sleep(120)
    if user_id in user_links:
        del user_links[user_id]
        bot.send_message(user_id, "⏳ Your link has expired! Request again later.")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    if not is_user_in_channel(user_id):
        bot.send_message(user_id, f"🚀 Please join our channel first: {CHANNEL_USERNAME}\nThen press /start again.")
        return

    # Check if the user already got a link
    if user_id in user_links:
        bot.send_message(user_id, "❌ You have already used your link. Wait for the next update.")
        return

    if gplink_url:
        unique_link = f"{gplink_url}?token={uuid.uuid4()}"  # Generate a unique link for the user
        user_links[user_id] = unique_link
        bot.send_message(user_id, f"🎉 Here is your unique link:\n{unique_link}\n\n⏳ This link will expire in 2 minutes.")
        threading.Thread(target=delete_user_link, args=(user_id,)).start()
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

bot.polling()
