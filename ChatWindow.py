import tkinter as tk
from datetime import datetime
import db
import tkinter.messagebox as tkmb

class ChatWindow(tk.Tk):
    def __init__(self, userid):
        super().__init__()
        self.userid = userid
        self.title("Chat Window")

        # Configure colors
        bg_color = "#F0F0F0"
        text_color = "#333333"
        button_color = "#007BFF"
        button_text_color = "white"

        # Create a frame for better organization
        self.frame = tk.Frame(self, bg=bg_color)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Text Area
        self.text_area = tk.Text(self.frame, wrap="word", bg="lightgray", fg=text_color, font=("Helvetica", 12))
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)

        # Send Button
        self.send_button = tk.Button(self.frame, text="Send", command=self.send_message, bg=button_color, fg=button_text_color, font=("Helvetica", 12))
        self.send_button.pack(side=tk.BOTTOM, pady=10, padx=10, ipadx=10, ipady=5)

    def send_message(self):
        mymessage = self.text_area.get("1.0", "end-1c")  # Get the message from the text area
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        connect = db.create_connection()
        with connect:
            cursor = connect.cursor()
            cursor.execute("Insert into data_transfer(userid, sended_at, message, status) values (?, ?, ?, ?)",
                           (self.userid, current_datetime, mymessage, False))
            connect.commit()
            tkmb.showinfo(title="Message Sent", message="Your message has been sent successfully.")

        self.destroy()
