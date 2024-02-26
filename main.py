import tkinter as tk
from tkinter import ttk

def open_new_window(userid):
    new_window = tk.Toplevel()
    new_window.title("Welcome Window")
    
    # Create a style
    style = ttk.Style()
    style.configure('TLabel', font=('Arial', 14))
    style.configure('TFrame', background='#f0f0f0')
    
    # Frame
    frame = ttk.Frame(new_window, padding=(20, 20))
    frame.pack(fill='both', expand=True)
    
    # Welcome Label
    welcome_label = ttk.Label(frame, text=f"Welcome! Your UserID is: {userid}")
    welcome_label.pack(pady=10)
    
    # Additional Labels
    label2 = ttk.Label(frame, text="Additional Information", font=('Arial', 12, 'bold'))
    label2.pack(pady=5)
    
    # Example of a button
    button = ttk.Button(frame, text='Close', command=new_window.destroy)
    button.pack(pady=10)
