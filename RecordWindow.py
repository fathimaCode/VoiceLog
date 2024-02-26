import tkinter as tk
from tkinter import ttk
import os
import tkinter.messagebox as tkmb
import db
import sounddevice as sd
import soundfile as sf
from PIL import Image, ImageTk
from threading import Thread
from datetime import datetime
class RecordWindow(tk.Toplevel):
    def __init__(self, userid):
        super().__init__()
        self.title("Record Audio")
        self.geometry("500x500")
        self.configure(bg="#000000")
        self.userid = userid
        # Set up styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#FFFFFF")
        self.style.configure("TButton", background="#007BFF", foreground="#000000")
        self.style.map("TButton", background=[("active", "#000000"), ("disabled", "#CCCCCC")], foreground=[("active", "#000000")])

        # Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create top frame for buttons
        top_frame = ttk.Frame(main_frame, padding=(20, 10))
        top_frame.pack(fill=tk.X)

        self.record_button = ttk.Button(top_frame, text="Start Recording", command=self.start_recording, style="TButton")
        self.record_button.pack(side=tk.LEFT)

        self.stop_button = ttk.Button(top_frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED, style="TButton")
        self.stop_button.pack(side=tk.LEFT, padx=10)

        # Create bottom frame for filename label and send button
        bottom_frame = ttk.Frame(main_frame, padding=(20, 0))
        bottom_frame.pack(fill=tk.X)

        self.filename_label = ttk.Label(bottom_frame, text="", background="#FFFFFF")
        self.filename_label.pack(side=tk.LEFT, expand=True)

        self.send_button = ttk.Button(bottom_frame, text="Send", command=self.send_recording, state=tk.DISABLED, style="TButton")
        self.send_button.pack(side=tk.LEFT)

        self.recording = False
        self.filename = ""

        # Center the window
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def start_recording(self):
        self.recording = True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.filename_label.config(text="Recording...")

        self.record_thread = Thread(target=self._start_recording)
        self.record_thread.start()

    def stop_recording(self):
        self.recording = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.send_button.config(state=tk.NORMAL)
        self.filename_label.config(text=f"Recording saved")

    def _start_recording(self):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"asset/records/incidient_{timestamp}.wav"
        with sf.SoundFile(self.filename, mode='w', samplerate=44100, channels=2) as file:
            with sd.InputStream(callback=lambda data, frames, time, status: file.write(data)):
                while self.recording:
                    sd.sleep(100)

    def send_recording(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        connect = db.create_connection()
        with connect:
            cursor = connect.cursor()
            cursor.execute("Insert into data_transfer(userid, sended_at, message, mode,status) values (?, ?, ?,?, ?)",
                           (self.userid, current_datetime, self.filename, True,False))
            connect.commit()
            tkmb.showinfo(title="Message Sent", message="Your message has been sent successfully.")


