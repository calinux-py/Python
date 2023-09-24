
## Project Overview:
This project is a Python script that uses the `discord.py` library to periodically fetch and send information about a game server's status to a Discord channel. The script retrieves the player count, server uptime, and world age from the specified BattleMetrics server page and sends this information to the specified Discord channel every two minutes.

## Requirements:
- Python 3.6 or higher
- Discord account
- Discord Bot Token
- Discord Channel ID
- `requests` library
- `beautifulsoup4` library
- `discord.py` library

## Installation:
1. Install the required Python packages.
    ```sh
    pip install requests beautifulsoup4 discord.py
    ```
2. Clone or download the Python script to your local machine.

## Setup:

1. **Create a Discord Bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications) and log in.
   - Create a new application and go to the "Bot" tab to create a new bot.
   - Copy the token provided under the "Bot" tab. This token is used to authenticate the bot with the Discord API.

2. **Invite the Bot to Your Server**
   - Go to the "OAuth2" tab in your bot's application page.
   - In the "OAuth2 URL Generator" section, select the "bot" scope.
   - Copy the generated URL and paste it into your web browser.
   - Select the server you want to invite the bot to and click "Authorize".

3. **Get Channel ID**
   - In Discord, go to your server settings -> Appearance -> Developer Mode and turn it on.
   - Right-click on the channel you want to send messages to and copy the ID.

4. **Configure the Python Script**
   - Replace `'YOUR DISCORD TOKEN'` in the script with the bot token you copied earlier.
   - Replace the `CHANNEL_ID` in the script with the ID of your Discord channel.
   - Optionally, replace the `URL` in the script with the URL of the BattleMetrics server page you are interested in.

## Running the Script:
Navigate to the directory where the script is located and run the following command:
```sh
python <script_name>.py
```

Replace `<script_name>` with the name of your Python script.

## Expected Output:
When the bot successfully logs in, it prints the following message to the console:
```
We have logged in as <bot_username>
```
The bot will then start sending server information to the specified Discord channel every two minutes.

## Note:
- Ensure that the bot has the necessary permissions to read and send messages in the specified channel.
- Handle the Discord bot token securely as it provides access to the bot’s functionalities.
- Be respectful and aware of the server's rules and guidelines, especially when scraping websites or interacting with Discord servers.
