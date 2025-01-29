from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import logging
import os

app = Flask(__name__)

# Get environment variables directly (Koyeb will inject them)
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
gplink = os.getenv('GPLINK')

# Initialize the bot and application
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to check if user is in the channel
def is_member(update: Update) -> bool:
    user_id = update.message.from_user.id
    try:
        chat_member = bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Start command handler
async def start(update: Update, context: CallbackContext):
    if is_member(update):
        message = f"Congratulations! You're already a member of the channel. Here is your gplink: {gplink}"
        await update.message.reply_text(message)
    else:
        keyboard = [[InlineKeyboardButton("Join Channel", url=f'https://t.me/{CHANNEL_ID[1:]}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Hey Buddy, if you want the gplink, you need to join my channel.", reply_markup=reply_markup)

# Admin command to update gplink
async def set_link(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        new_link = ' '.join(context.args)
        if new_link:
            global gplink
            gplink = new_link
            await update.message.reply_text(f"gplink has been updated to: {gplink}")
        else:
            await update.message.reply_text("Please provide a new gplink URL.")
    else:
        await update.message.reply_text("You are not authorized to change the gplink.")

# Flask route to handle webhook
@app.route('/webhook', methods=['POST'])
async def webhook():
    if request.method == "POST":
        json_str = request.get_data(as_text=True)
        update = Update.de_json(json_str, bot)
        application.process_update(update)
        return "ok", 200

# Set the webhook URL for your bot
def set_webhook():
    url = f"https://yourdomain.com/webhook"
    bot.set_webhook(url)

# Main function to run the bot
if __name__ == '__main__':
    # Set the webhook URL when the app starts
    set_webhook()

    # Add command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('setlink', set_link, pass_args=True))

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)  # You can change the port as needed
