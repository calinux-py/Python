# VoiceLogger

VoiceLogger is a Python script that utilizes the Speech Recognition library to convert spoken words into text and sends this text to a Discord channel through a webhook.

## Features

- Real-time speech recognition.
- Sends recognized text to Discord via webhook.
- Runs continuously in the background.
- Error handling for speech recognition failures.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6+
- `speech_recognition` library
- `requests` library

## Installation

1. Clone the repository or download the `VoiceLogger.py` script.
2. Install the required Python libraries using pip:
   ```sh
   pip install speech_recognition requests
   ```

## Configuration

1. Replace `'YOUR DISCORD WEBHOOK'` with your Discord webhook URL in the `WEBHOOK_URL` variable.
2. Set the `SEND_INTERVAL` to the desired time interval (in seconds) for sending text to Discord.

## Usage

To start the VoiceLogger, run the script in your terminal:

```sh
python VoiceLogger.py
```

The script will start listening to your default microphone and will send the recognized text to the specified Discord webhook every `SEND_INTERVAL` seconds.
