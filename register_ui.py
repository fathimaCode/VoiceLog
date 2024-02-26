import customtkinter as ctk
import tkinter.messagebox as tkmb
import db
import os

def redirect_to_login():
    app.destroy()
    os.system("python login_ui.py") 

def handle_login():
    username = user_entry.get()
    email = email_entry.get()
    pwd = pwd_entry.get()
    
    # Validate input
    if not all((username, email, pwd)):
        tkmb.showerror(title="Error", message="Please fill in all fields.")
        return
    
    # Insert data into the database
    connect = db.create_connection()
    if connect is not None:
        with connect:
            cursor = connect.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, pwd))
            connect.commit()
        tkmb.showinfo(title="Registration Successful", message="Your account has been created successfully.")
        redirect_to_login()
    else:
        tkmb.showerror(title="Database Error", message="Failed to connect to the database.")

# Set GUI theme
ctk.set_appearance_mode("light")

app = ctk.CTk()
app.iconbitmap('asset/logo.ico')
app.geometry("500x500")
app.title("Welcome to Speakify")

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text="Create an account", font=("Arial", 18))
label.pack(pady=20, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=10, padx=10, fill='x')

email_entry = ctk.CTkEntry(master=frame, placeholder_text="Email Address")
email_entry.pack(pady=10, padx=10, fill='x')

pwd_entry = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
pwd_entry.pack(pady=10, padx=10, fill='x')

loginBtn = ctk.CTkButton(master=frame, text="Create an account", text_color="white",
    hover= True,
    hover_color= "black",
    height=35,
    width= 120,
    border_width=2,
    corner_radius=4,
    border_color= "#5d6266", 
    bg_color="#252525",
    fg_color= "#262626", command=handle_login)
loginBtn.pack(pady=20, padx=10, fill='x')
registerBtn = ctk.CTkButton(master=frame, text="Login", command=redirect_to_login)
registerBtn.pack(pady=20, padx=10)




app.mainloop()
