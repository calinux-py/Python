# Movie Guru with OpenAI API
![](https://img.shields.io/badge/-Python-purple)
![](https://img.shields.io/badge/-Windows-yellow)

This Python script provides movie recommendations based on user-supplied tags. It uses PyQt5 for the GUI and the OpenAI API for generating the recommendations.

## Features

- Minimalistic user interface for easier navigation.
- Support for multiple tags to refine movie recommendations.
- Settings window to enter and update the OpenAI API Key.
- Retry option to search for a new set of movie recommendations.

## Requirements

- Python 3.x
- PyQt5
- OpenAI Python package
- configparser

## Installation

### Install Dependencies

Run the following command to install the required packages.

```bash
pip install PyQt5 openai configparser
```

## Usage

1. Start the application by running `python your_script_name.py`.
2. Click on the "Settings" button to enter your OpenAI API key.
3. Enter tags separated by commas into the input field.
4. Click on "Search Movies" to receive a list of recommended movies.
5. Optionally, click "Search Again" to get a new list based on the same tags.

## Configuration

The OpenAI API key is stored in `config.ini`. You can manually edit this file, or you can use the Settings window in the app to update the key.

```ini
[OpenAI]
api_key = YOUROPENAIAPI
```

## How it Works

The application has two primary components:

### SettingsWindow

This class handles the functionality for storing the OpenAI API Key. When you click 'Save', it updates the API key in the `config.ini` file.

### MovieApp

This class handles the main application logic. It allows the user to input tags for movie recommendations, sends a request to OpenAI based on the tags, and displays the returned movie recommendations.



## Author

CaliNux

---
