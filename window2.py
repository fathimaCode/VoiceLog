import tkinter as tk
from tkinter import ttk
import os
from messagewindow import MessageWindow
from ChatWindow import ChatWindow
from MyMailsWindow import MyMailsWindow
from RecordWindow import RecordWindow
class Window2(tk.Tk):
    def __init__(self, userid, username):
        super().__init__()
        self.title("Incidient Reporting System")
        self.geometry("800x800")  # Set window size
        self.configure(bg="#F0F0F0")  # Set background color

        # Welcome label
        self.label = tk.Label(self, text=f"Welcome, {username}!", bg="#007BFF", fg="white", font=("Helvetica", 16))
        self.label.pack(fill=tk.X, padx=10, pady=10)

        # Create a frame to contain the buttons
        frame = tk.Frame(self, bg="#F0F0F0")
        frame.pack(fill=tk.BOTH, expand=True)

        # Load and resize images
        home_image = tk.PhotoImage(file="asset/record.png").subsample(2, 2)
        profile_image = tk.PhotoImage(file="asset/mymail.png").subsample(2, 2)
        chat_image = tk.PhotoImage(file="asset/message.png").subsample(2, 2)
        message_image = tk.PhotoImage(file="asset/mic.png").subsample(2, 2)
        logout_image = tk.PhotoImage(file="asset/logout.png").subsample(2, 2)
        centerImage = tk.PhotoImage(file="asset/bg.png").subsample(1,1)
        # Create labels and buttons with images
        home_label = tk.Label(frame, image=home_image, text="Report by Records", compound=tk.TOP, bg="#F0F0F0")
        profile_label = tk.Label(frame, image=profile_image, text="Reported Incidents", compound=tk.TOP, bg="#F0F0F0")
        chat_label = tk.Label(frame, image=chat_image, text="Report by Text", compound=tk.TOP, bg="#F0F0F0")
        message_label = tk.Label(frame, image=message_image, text="Report by Voice", compound=tk.TOP, bg="#F0F0F0")
        logout_label = tk.Label(frame, image=logout_image, text="Log out", compound=tk.TOP, bg="#F0F0F0")
        center_label = tk.Label(frame, image=centerImage, text="", compound=tk.TOP, bg="#F0F0F0")

        # Grid the labels and buttons inside the frame
        home_label.grid(row=0, column=1, padx=150, pady=10,sticky="nsew")
        profile_label.grid(row=0, column=2, padx=150, pady=10,sticky="nsew")
        message_label.grid(row=0, column=3, padx=5, pady=10,sticky="nsew")
        center_label.grid(row=1, column=0, columnspan=5, padx=350, pady=50,sticky="nsew")
        chat_label.grid(row=2, column=1, padx=150, pady=10,sticky="nsew")
        logout_label.grid(row=2, column=2, padx=10, pady=10,sticky="nsew")

        
        self.home_image = home_image
        self.profile_image = profile_image
        self.message_image = message_image
        self.logout_image = logout_image
        self.chat_image = chat_image
        self.centerImage = centerImage
        self.userid = userid  # Store userid for later use

        # Bind events to buttons
        logout_label.bind("<Button-1>", self.logout)
        message_label.bind("<Button-1>", self.open_message_window)
        home_label.bind("<Button-1>", self.open_recordMsg)
        chat_label.bind("<Button-1>", self.open_chat_window)
        profile_label.bind("<Button-1>", self.open_mymail_window)
     

    def logout(self, event):
        self.destroy()
        os.system("python login_ui.py")
    


    def open_recordMsg(self,event):
        record_window = RecordWindow(self.userid)  
        record_window.mainloop()

    def open_message_window(self, event):
        message_window = MessageWindow(self.userid)  # Pass userid to MessageWindow
        message_window.mainloop()
   
    def open_chat_window(self, event):
        chat_window = ChatWindow(self.userid)  
        chat_window.mainloop()
        
    def open_mymail_window(self, event):
        mymail_window = MyMailsWindow(self.userid)  
        mymail_window.mainloop()

def open_new_window(userid):
    window2 = Window2(userid)
    window2.mainloop()
