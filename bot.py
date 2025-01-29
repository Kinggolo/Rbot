import telebot
import threading
import time
import uuid
import os

# Use environment variables for security
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Store the bot token in environment variables
CHANNEL_USERNAME = "@speedy_current_affairs_2026"  # Your channel's username
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Store your admin ID in environment variables

bot = telebot.TeleBot(TOKEN)
gplink_url = None  # GPLink URL that the admin will update
user_links = {}  # Dictionary to store user-specific links

def is_user_in_channel(user_id):
    """Check if the user is a member of the specified channel"""
    try:
        chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def send_user_message(user_id, message):
    """Send a message to the user"""
    bot.send_message(user_id, message)

def delete_expired_links():
    """Periodically check and delete expired links"""
    while True:
        current_time = time.time()
        expired_users = [user_id for user_id, (link, timestamp) in user_links.items() if current_time - timestamp > 120]
        
        for user_id in expired_users:
            del user_links[user_id]
            send_user_message(user_id, "⏳ Your link has expired! Request again later.")
        
        time.sleep(60)  # Check every 60 seconds

# Start the expiration checker in a separate thread
threading.Thread(target=delete_expired_links, daemon=True).start()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    if not is_user_in_channel(user_id):
        send_user_message(user_id, f"🚀 Please join our channel first: {CHANNEL_USERNAME}\nThen press /start again.")
        return

    # Check if the user already got a link
    if user_id in user_links:
        send_user_message(user_id, "❌ You have already used your link. Wait for the next update.")
        return

    if gplink_url:
        unique_link = f"{gplink_url}?token={uuid.uuid4()}"
        user_links[user_id] = (unique_link, time.time())  # Store the link and its creation time
        send_user_message(user_id, f"🎉 Here is your unique link:\n{unique_link}\n\n⏳ This link will expire in 2 minutes.")
    else:
        send_user_message(user_id, "❌ No link is available right now. Please wait for the admin to update.")

@bot.message_handler(commands=['setlink'])
def set_link(message):
    global gplink_url
    if message.chat.id == ADMIN_ID:
        new_link = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
        if new_link:
            gplink_url = new_link
            send_user_message(ADMIN_ID, f"✅ GPLink updated to: {gplink_url}")
        else:
            send_user_message(ADMIN_ID, "❌ Please provide a valid link. Example:\n/setlink https://newgplink.com")
    else:
        send_user_message(message.chat.id, "❌ You are not authorized to use this command.")

bot.polling()
