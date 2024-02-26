import tkinter as tk
from tkinter import PhotoImage

def on_button_click():
    print("Button clicked")

root = tk.Tk()
root.title("Grid with Icons")

# Define button size
button_width = 200
button_height = 200

# Load icon image
icon_image = PhotoImage(file="asset/home.png")  # Replace "icon.png" with your icon file path
icon_image1 = PhotoImage(file="asset/message.png") 
# Create buttons
button1 = tk.Button(root, image=icon_image, command=on_button_click, width=button_width, height=button_height)
button2 = tk.Button(root, image=icon_image, command=on_button_click, width=button_width, height=button_height)
button3 = tk.Button(root, image=icon_image1, command=on_button_click, width=button_width, height=button_height)
button4 = tk.Button(root, image=icon_image, command=on_button_click, width=button_width, height=button_height)
# Place buttons in grid
button1.grid(row=0, column=0)
button2.grid(row=0, column=1)
button3.grid(row=0, column=2)
button4.grid(row=1, column=0)
root.mainloop()
