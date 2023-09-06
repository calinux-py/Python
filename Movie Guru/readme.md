# Movie Guru with OpenAI API
![](https://img.shields.io/badge/-Python-purple)
![](https://img.shields.io/badge/-Windows-yellow)

## Overview

This Python script uses PyQt5 for GUI and OpenAI API to generate movie recommendations based on user input tags. Users can search for movies, see search history, and export their history to a text file. The script also allows users to manage their OpenAI API key via a settings window.

## Features

- Search for movie recommendations based on tags
- View search history
- Export search history
- Add new tags to enhance search functionality
- Manage OpenAI API key through a settings window

## Installation

1. Install the required Python packages:

    ```
    pip install PyQt5 openai configparser
    ```

2. Create a `config.ini` file in the same directory as your script with the following format:

    ```
    [OpenAI]
    api_key = your-openai-api-key-here
    ```

## How to Run

1. Navigate to the directory containing the script.

2. Run the script:

    ```
    python your-script-name.py
    ```

## Usage

1. **Search for Movies**: Enter tags separated by commas and click on `Search Movies`.

2. **History**: Click on `History` to view your search history.

3. **Export**: Click on `Export` to export your search history to a text file on your Desktop.

4. **Settings**: Click on `Settings` to open the settings window where you can update your OpenAI API key.


## Author

CaliNux

---
