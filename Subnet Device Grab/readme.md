# Subnet Scanner and Discord Uploader
![](https://img.shields.io/badge/-Python-purple)
![](https://img.shields.io/badge/-Windows-yellow)


This Python script allows you to scan the devices connected to your local network subnet and upload the results to a Discord channel using a webhook. The script utilizes `netifaces`, `scapy`, and `requests` modules to achieve this functionality.

## Installation

To install the required modules, use the following pip command:

```bash
pip install netifaces scapy requests
```

Please make sure you have Python installed on your system before running the installation command.

## Configuration

Before running the script, you need to set up your Discord webhook URL. Replace the placeholder `"YOUR DISCORD WEBHOOK HERE"` in the script with your actual webhook URL. The script will use this URL to upload the scan results to your designated Discord channel.

## How to Use

1. Open a terminal or command prompt.

2. Navigate to the directory where you saved the Python script.

3. Run the script using Python:

```bash
python subnet_scanner_discord.py
```

4. The script will scan your local network subnet, identify the devices connected to it, and generate a file named `subnet_devices.txt` in your system's temporary directory. The output will also be displayed on the console.

5. The script will then upload the `subnet_devices.txt` file to the configured Discord channel using the webhook URL.

6. You can check your Discord channel to view the uploaded file and see the list of devices on your network subnet.

## Important Note

Please ensure that you have the necessary permissions to upload files to the Discord channel using the webhook. If you encounter any issues during the script execution or upload process, check your Discord webhook settings and permissions.

## Disclaimer

This script is intended for educational and informational purposes only. Use it responsibly and only on networks you have authorization to scan. The author and contributors are not responsible for any misuse or illegal activities conducted with this script.
