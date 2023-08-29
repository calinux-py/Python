# Screenshot Bot - Discord Webhook Automation
![](https://img.shields.io/badge/-Python-purple)
![](https://img.shields.io/badge/-Windows-yellow)


## Overview

Screenshot Bot is a Python script designed to capture and share screenshots of specified websites to a Discord channel using a webhook. It utilizes various Python libraries like `webbrowser`, `time`, `pyautogui`, `os`, and `requests` to automate the process of opening web pages, capturing screenshots, and sending them to a Discord webhook.
This script is used by flipper and powershell payloads.

Ducky Script uses irm request to call PowerShell script, which downloads python, dependencies, etc, and then finally downloads this script and runs.

## Prerequisites

- Python 3.x installed on your system.
- Python libraries: `webbrowser`, `time`, `pyautogui`, `os`, `requests`.
- A Discord account and access to a Discord server with the appropriate permissions to create and use a webhook URL.

## Setup

1. Install Python 3.x: Make sure you have Python 3.x installed on your system. You can download it from the official Python website.

2. Install required libraries: Open a terminal or command prompt, navigate to the directory containing the script, and run the following command to install the necessary libraries:

   ```bash
   pip install requests
   ```

3. Obtain Discord Webhook URL: Create a new webhook on your Discord server by following these steps:
   - Go to your Discord server settings.
   - Click on the "Integrations" tab.
   - Select "Webhooks" and click "Create Webhook."
   - Customize the webhook settings (name, avatar, etc.) and copy the webhook URL.

4. Update the script: Replace `'YOUR DISCORD WEBHOOK'` in the script with the actual Discord webhook URL you obtained in the previous step.

## How to Use

1. Define the list of URLs: Modify the `urls` list in the script with the URLs you want to capture screenshots of.

2. Run the script: Save the script and run it using the following command:

   ```bash
   python screenshot_bot.py
   ```

3. Execution: The script will open each URL in a browser tab, capture a screenshot of the page, save it temporarily, and then send all the screenshots as attachments to the specified Discord webhook.

4. Discord Channel: The screenshots will be posted in the Discord channel connected to the webhook. The bot will post the screenshots with a message that says "Screenshots for URLs:".

## Important Notes

- The script captures the first URL separately and then captures the remaining URLs concurrently using a ThreadPoolExecutor for faster processing.
- The script uses `pyautogui` to control the browser and capture screenshots. Make sure the browser window is visible and accessible during script execution.
- Use this script responsibly and ensure you have permission to capture screenshots of the websites you are targeting.
