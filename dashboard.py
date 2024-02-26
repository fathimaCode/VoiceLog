import tkinter as tk

class DashboardFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(bg='white')
        label = tk.Label(self, text="Dashboard", font=("Helvetica", 24))
        label.pack(pady=20)
