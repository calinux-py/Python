# PyRate YouTube Downloader & PyRate Converter

This repository contains two Python scripts for downloading YouTube videos and converting video files to various formats using PyQt5. `PyRate YouTube Downloader` allows you to download YouTube videos with different quality options. `PyRate Converter` enables you to convert video files to different formats.

## Table of Contents
1. [Installation](#installation)
    - [PyRate YouTube Downloader](#pyrate-youtube-downloader)
    - [PyRate Converter](#pyrate-converter)

## Installation

To run the scripts, make sure you have the following Python libraries installed. You can install them using pip:

```shell
pip install PyQt5 moviepy yt-dlp
```

### PyRate YouTube Downloader

To start the YouTube downloader, navigate to the directory containing the scripts and run:

```shell
python PYrateGUI.py
```

#### Instructions
1. Enter the YouTube URL in the input box.
2. Select the desired quality option.
3. Click on the 'Download' button.
4. Downloaded videos will be stored in the `Downloads` directory of the user's home directory.

### PyRate Converter

To start the converter, navigate to the directory containing the scripts and run:

```shell
python convert.py
```

#### Instructions
1. Click 'Browse' to select a video file.
2. Choose the desired output format from the dropdown menu.
3. Click 'Convert' to start the conversion.
4. After conversion, the original file will be replaced with the converted one.
