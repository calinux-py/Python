# LetsMeet - Discord Meeting Scheduler

## Overview

LetsMeet is a Discord bot script designed to facilitate scheduling meetings within a Discord server. The script integrates with the Discord API to provide an interactive and user-friendly interface for creating and managing meetings.

## Features

- **Meeting Scheduling**: Users can schedule new meetings with date, time, and timezone details.
- **Timezone Support**: Includes support for various timezones, automatically converting meeting times to different zones.
- **Interactive Modals**: Utilizes Discord's modal interface for inputting meeting details.
- **Automatic Notifications**: Sends scheduled meeting details to a specified channel, including reactions for RSVP.

## Requirements

- Python 3.8 or higher
- Discord API library (`discord.py`)
- `pytz` for timezone handling

## Installation

1. Clone the repository or download the script.
2. Install the required libraries using `pip`:
   ```
   pip install discord pytz
   ```
3. Set up a Discord bot account and retrieve the token.

## Usage

1. Insert your Discord bot token at the end of the script.
2. Run the script using Python.
3. In Discord, use the `/new` command to schedule a meeting.

## Setting Up the Bot

- Replace `channel_id` in the script with the ID of the Discord channel where meeting notifications should be sent.
- Use the Discord Developer Portal to set up and invite your bot to your server.

## License

LetsMeet is released under the [MIT License](https://opensource.org/licenses/MIT).
