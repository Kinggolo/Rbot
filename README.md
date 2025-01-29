# Telegram Bot Project

This project creates a Telegram bot that provides users with a one-time-use link to a specified GPLink URL. 

## Features
- **Channel Join Requirement**: Users must join a specific Telegram channel before they can access the GPLink URL.
- **Unique Links**: Each user receives a unique, one-time-use link that expires after 2 minutes.
- **Admin Control**: The admin can manually update the GPLink URL using the `/setlink <new_link>` command.

## Setup

1. **Install Dependencies**:
    - Create a virtual environment (optional but recommended):
      ```bash
      python3 -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
      ```

    - Install required dependencies:
      ```bash
      pip install -r requirements.txt
      ```

2. **Configuration**:
    - Replace the `YOUR_BOT_TOKEN` with your Telegram bot token.
    - Set your Telegram channel username in the `CHANNEL_USERNAME` variable.
    - Set your Telegram user ID in the `ADMIN_ID` variable to allow manual link updates.

3. **Run the Bot**:
    - Run the bot locally:
      ```bash
      python bot.py
      ```

4. **Deploy on Koyeb**:
    - Follow the Koyeb deployment steps to deploy your bot.
    - Make sure to use the `Procfile` for the correct deployment configuration.

## Commands
- **/start**: Starts the bot and checks if the user has joined the channel, then provides a unique link.
- **/setlink <new_link>**: Allows the admin to set a new GPLink URL.
