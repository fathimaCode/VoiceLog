import tkinter as tk

class ProfileFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='white')
        label = tk.Label(self, text="Profile", font=("Helvetica", 24))
        label.pack(pady=20)
