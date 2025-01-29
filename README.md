# Telegram Bot with GP Link and Channel Verification

**Version**: 1.0.0

This is a simple Telegram bot that allows users to get a unique GP link after joining a specific Telegram channel. The bot provides the GP link via an inline button, and the link expires after 2 minutes. Admins can update the GP link anytime, and users can request their link by interacting with the bot.

---

## Features

- **Channel Verification**: The bot verifies whether the user has joined a specific channel before giving access to the GP link.
- **Unique GP Link**: The bot generates a unique GP link for each user, which expires in 2 minutes.
- **Inline Buttons**: The bot uses inline buttons for easy access to the channel and the GP link.
- **Admin Control**: The admin can update the GP link using the `/setlink` command.
- **Link Expiration**: The links expire after 2 minutes, and expired links are automatically deleted.
- **Health Check**: The bot includes a health check endpoint for monitoring.

---

## Setup

### Prerequisites

- Python 3.x
- Telegram Bot Token
- A Telegram Channel (set to public)

### Installation Steps

1. **Clone the repository**:
    ```bash
    git clone (https://github.com/Kinggolo/Telegram-Channel-Force-Bot.git)
    cd Telegram-Channel-Force-Bot
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file and add the following environment variables:
    ```
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    ADMIN_ID=your_telegram_admin_user_id
    CHANNEL_USERNAME=your_channel_id
    ```

4. **Run the bot**:
    Start the bot and the health check Flask app by running:
    ```bash
    python bot.py
    ```

5. **Access Health Check**:
    The bot will also run a Flask app that you can use to monitor the health of the service. The health check endpoint will be available at:
    ```
    http://localhost:5000/health
    ```

---

## Commands

- `/start`: Checks if the user has joined the channel and provides a unique GP link (if available).
- `/setlink [URL]`: Admin command to update the GP link. Example:
    ```
    /setlink https://newgplink.com
    ```

---

## Bot Flow

1. **User starts interaction**:
   - The user sends the `/start` command.
   - The bot checks if the user is a member of the required channel.
     - If the user is not in the channel, a "Join Channel" button is sent to the user.
     - If the user is in the channel, a "Get GPLink" button is sent with the unique GP link.

2. **Admin updates the GP link**:
   - The admin uses `/setlink [URL]` to update the link.
   - The new link is stored and available for all users until it expires.

3. **Link Expiration**:
   - Each generated link expires after 2 minutes.
   - After the expiration time, the link is removed from the system, and the user is notified.

---

## Deployment

For deployment, you can host the bot on a cloud platform such as Heroku, AWS, or DigitalOcean. Make sure to expose the bot's health check URL for monitoring.

---

## Contributing

We welcome contributions to this project! If you would like to contribute, please fork the repository and submit a pull request.

---

## License

This project is open source and available under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

## Acknowledgments

- Thanks to [Python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the powerful Telegram bot library.
- Thanks to [Flask](https://flask.palletsprojects.com/) for the health check API.

---

## Screenshots

If you'd like to include any screenshots of the bot in action, you can add them here!
