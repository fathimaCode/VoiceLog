import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time

def redirect_to_login():
    root.destroy()
    os.system("python login_ui.py")

def update_icon_position(event=None):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    icon_label.place(relx=0.5, rely=0.5, anchor="center")

root = tk.Tk()
root.title("Speakify")
root.geometry("500x500")
root.iconbitmap('asset/logo.ico')
root.configure(bg="#00BDFF")

# Load and resize the image
icon_image = Image.open("asset/logo.png")
icon_image = icon_image.resize((100, 100), Image.ANTIALIAS)
icon_photo = ImageTk.PhotoImage(icon_image)

# Create a label with the resized image
icon_label = ttk.Label(root, image=icon_photo)
icon_label.image = icon_photo

# Create a label with "Speakify" text
speakify_label = ttk.Label(root, text="Speakify", font=("Arial", 20))

icon_label.place(relx=0.5, rely=0.4, anchor="center")
speakify_label.place(relx=0.5, rely=0.6, anchor="center")  # Adjusted the rely parameter
root.bind("<Configure>", update_icon_position)
root.after(5000, redirect_to_login)  # Changed to 5000 milliseconds

root.mainloop()
