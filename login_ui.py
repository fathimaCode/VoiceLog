import customtkinter as ctk
import tkinter.messagebox as tkmb
import os
import db

from window2 import Window2  # Importing Window2 directly from main

db.create_database()

app = ctk.CTk()
app.iconbitmap('asset/logo.ico')
app.geometry("500x500")  # Setting the window size to 500x500
app.title("Welcome to Speakify")

# Create a frame to contain the login interface
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text="Login", font=("Arial", 18))
label.pack(pady=20, padx=10)

user_entry = ctk.CTkEntry(master=frame,  width= 345,
    height=35, placeholder_text="Email Address")
user_entry.pack(pady=20, padx=10)

pwd_entry = ctk.CTkEntry(master=frame, width= 345,
    height=35, placeholder_text="Password", show="*")
pwd_entry.pack(pady=20, padx=10)

def handle_login():
    email = user_entry.get()
    pwd = pwd_entry.get()
    if(email=="hr1@speakify.com" and pwd=="hr1"):
        redirect_to_hr1()
    elif(email=="hr2@speakify.com" and pwd=="hr2"):
        redirect_to_hr2()
    else:
        connect = db.create_connection()
        userid = 0
        username=''
        if connect is None:
            tkmb.showerror(title="Database Error", message="Failed to connect to the database")
            return

        with connect:
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM users where email=? and password=?", (email, pwd))
            rows = cursor.fetchall()
            if not rows:
                tkmb.showerror(title="There is no data available", message="Invalid email or password")
                return
            for row in rows:
                print(row)
                userid = row[0]
                username = row[1]
        print("myuserid 45:",userid)
        if userid > 0:
            tkmb.showinfo(title="Login Successfully", message="You have logged in successfully")
            redirect_to_dashboard(userid,username)
        else:          
            tkmb.showerror(title="Login Error", message="Invalid user ID")


def redirect_to_registration():
    app.destroy()
    os.system("python register_ui.py")

def redirect_to_hr1():
    app.destroy()
    os.system("python hr1.py")

def redirect_to_hr2():
    app.destroy()
    os.system("python hr2.py")

def redirect_to_dashboard(userid,username):
    app.destroy()
    if(userid!=0):
        print("line     47:",userid)
        window2 = Window2(userid,username)  # Pass the userid to Window2 directly
        window2.mainloop()
    else:
        print('something went wrong')



loginBtn = ctk.CTkButton(master=frame, text="Login", text_color="white",
    hover= True,
    hover_color= "black",
    height=35,
    width= 120,
    border_width=2,
    corner_radius=4,
    border_color= "#5d6266", 
    bg_color="#252525",
    fg_color= "#262626",
 command=lambda: handle_login())
loginBtn.pack(pady=20, padx=10)

registerBtn = ctk.CTkButton(master=frame, text="Create an account", command=redirect_to_registration)
registerBtn.pack(pady=20, padx=10)

app.mainloop()
