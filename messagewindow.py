import tkinter as tk
import tkinter.messagebox as tkmb
import speech_recognition as sr
from datetime import datetime
import db


class MessageWindow(tk.Tk):
    def __init__(self, userid):
        super().__init__()
        self.title("Voice to text Conversion")
        self.geometry("500x400")
        self.userid = userid

        # Create a frame for better organization
        self.frame = tk.Frame(self, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Welcome Label
        self.label = tk.Label(self.frame, text=f"Welcome to Message Window! Your UserID is: {userid}", bg="lightblue", fg="black", font=("Helvetica", 14))
        self.label.pack(pady=10)

        # Text Area
        self.text_area = tk.Text(self.frame, height=15, width=50)
        self.text_area.pack(pady=10, padx=10)

        # Buttons Frame
        self.button_frame = tk.Frame(self.frame, bg="white")
        self.button_frame.pack()

        # Listen Button
        self.listen_button = tk.Button(self.button_frame, text="Start Listening", command=self.start_listening, bg="green", fg="white", font=("Helvetica", 12))
        self.listen_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Send Button
        self.send_button = tk.Button(self.button_frame, text="Send", command=self.send_message, state="disabled", bg="blue", fg="white", font=("Helvetica", 12))
        self.send_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Speech Recognition Initialization
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False

    def start_listening(self):
        self.listening = True
        self.listen_button.config(state="disabled")
        while self.listening:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                audio = self.recognizer.listen(source)

            try:
                print("Recognizing...")
                text = self.recognizer.recognize_google(audio)  # Recognize speech using Google Speech Recognition
                print("You said:", text)
                self.text_area.insert(tk.END, f"{text}\n")

                if self.text_area.get("1.0", "end-1c"):  # Check if text area is not empty
                    self.listen_button.config(state="disabled")
                    self.send_button.config(state="normal")
                break  # Stop listening after recognition
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said.")
                self.text_area.insert(tk.END, "Sorry, I could not understand what you said.\n")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                self.text_area.insert(tk.END, f"Error: {e}\n")

    def send_message(self):
        text = self.text_area.get("1.0", tk.END).strip()
        # Print user ID and recognized text
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        connect = db.create_connection()
        with connect:
            cursor = connect.cursor()
            cursor.execute("Insert into data_transfer(userid, sended_at, message, status)values(?,?,?,?)",
                           (self.userid, current_datetime, text, False))
            connect.commit()
            tkmb.showinfo(title="Mail sended Successfully", message="Mail send to HR")
        print("UserID:", self.userid)
        print("Recognized Text:", text)
        self.destroy()


if __name__ == "__main__":
    #userid = "YourUserID"  # Set your user ID here
    app = MessageWindow(userid)
    app.mainloop()
