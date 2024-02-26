import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tkmb
import db  
import shutil 
from datetime import datetime
import csv
import os
def open_download_window(did):
    print("i am audio download btn",did)
    with connect:
        cursor = connect.cursor()
        # Fetch data_transfer entries
        cursor.execute("SELECT * FROM data_transfer WHERE did=?", (did,))
        transfers = cursor.fetchall()
        for row in transfers:
            file_path = row[3]
            print(row[3])
            print("Downloading audio file:", file_path)
            destination = "downloads/downloaded_audio.wav"
            try:
                
                shutil.copy(file_path, destination)
                print("Audio file downloaded successfully.")
            except Exception as e:
                print("Error downloading audio file:", e)

def open_response_window(did):
    def send_response():
        # Get the content from the text area
        response_content = response_text.get("1.0", "end-1c")  # Get the text from the text area
        hrid = 1
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        connect = db.create_connection()
        with connect:
            cursor = connect.cursor()
            cursor.execute("Insert into messages(did,responded_id,message,updated_at, status)values(?,?,?,?,?)",(did,hrid,response_content,current_datetime,True))
            cursor.execute("UPDATE data_transfer SET status = ? WHERE did = ?", (True, did))
            connect.commit()
            tkmb.showinfo(title="Responded Successfully",message="Mail send")
        # Print the did and the text message
        print("Data Transfer ID:", did)
        print("Text Message:", response_content)

    response_window = tk.Toplevel(root)

    response_text = tk.Text(response_window, height=10, width=50)
    response_text.pack()

    send_button = tk.Button(response_window, text="Send", command=send_response, bg="green", fg="white")
    send_button.pack()

def download_report(connect):
    with connect:
        cursor = connect.cursor()

        # Fetch data_transfer entries
        cursor.execute("SELECT u.username, u.email, dt.sended_at, dt.message, dt.status AS data_transfer_status, m.message AS response_message, m.responded_id AS responded, m.updated_at AS response_updated_at, m.status AS message_status FROM users u JOIN data_transfer dt ON u.uid = dt.userid LEFT JOIN messages m ON dt.did = m.did")
        transfers = cursor.fetchall()

        # Write data to a CSV file
        with open("data_transfer_report.csv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            # Write column names
            csv_writer.writerow(['Username', 'Email', 'Sent At', 'Message', 'Data Transfer Status', 'Response Message', 'Responded','Response Updated At'])
            # Write data rows
            for row in transfers:
                message_status=''
                if row[4]==1:
                    message_status="responded"
                else:
                    message_status="No response"
                # Mapping responded_id to corresponding email addresses
                responded_email = ''
                if row[6] == 1:  # Index 6 corresponds to 'responded' column
                    responded_email = 'hr1@speakify.com'
                elif row[6] == 2:  # Index 6 corresponds to 'responded' column
                    responded_email = 'hr2@speakify.com'
                print(row)
                # Writing data row with responded email
                csv_writer.writerow([row[0], row[1], row[2], row[3], message_status, row[5],responded_email, row[7]])  # Excluding 'responded' column and replacing with 'responded_email'
        
        tkmb.showinfo(title="Downloaded Successfully", message="Report downloaded as 'data_transfer_report.csv'")

def display_data_transfer(connect):
    with connect:
        cursor = connect.cursor()

        # Fetch data_transfer entries
        cursor.execute("SELECT * FROM data_transfer where status = 0")
        transfers = cursor.fetchall()

        # Create a Treeview widget to display data
        frame = tk.Frame(root)
        frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        tree = ttk.Treeview(frame, columns=('did','userid', 'Sent At', 'Message','mode', 'Data Transfer Status'), show='headings')
        tree.pack(side="left", fill="both", expand=True)

        # Define column headings
        tree.heading('userid', text='userid')
        tree.heading('Sent At', text='Sent At')
        tree.heading('Message', text='Message')
        tree.heading('mode', text='mode')
        tree.heading('Data Transfer Status', text='Data Transfer Status')

        # Create a vertical scrollbar
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.pack(side="right", fill="y")

        # Configure Treeview to use vertical scrollbar
        tree.configure(yscrollcommand=vsb.set)

        # Create a horizontal scrollbar
        hsb = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
        hsb.grid(row=2, column=0, columnspan=3, sticky="ew")

        # Configure Treeview to use horizontal scrollbar
        tree.configure(xscrollcommand=hsb.set)

        for transfer in transfers:
            # Insert each transfer data into the treeview
            tree.insert('', 'end', values=transfer[1:])

            # Create a response button for each transfer
            response_button = tk.Button(root, text="Response", command=lambda did=transfer[0]: open_response_window(did), bg="blue", fg="white")
            response_button.grid(row=2+len(transfers), column=0, pady=5)
            response_button = tk.Button(root, text="Download Audio", command=lambda did=transfer[0]: open_download_window(did), bg="green", fg="white")
            response_button.grid(row=2+len(transfers), column=1, pady=5)

def display_responded_data():
    responded_window = tk.Toplevel(root)
    responded_window.title("Responded Data")
    
    with connect:
        cursor = connect.cursor()

        # Fetch responded data_transfer entries
        cursor.execute("SELECT u.username, u.email, dt.sended_at, dt.message, dt.status AS data_transfer_status, m.message AS response_message, m.responded_id AS responded, m.updated_at AS response_updated_at, m.status AS message_status FROM users u JOIN data_transfer dt ON u.uid = dt.userid LEFT JOIN messages m ON dt.did = m.did WHERE dt.status = 1")
        responded_transfers = cursor.fetchall()

        # Create a Treeview widget to display responded data
        responded_tree = ttk.Treeview(responded_window, columns=('Username', 'Email', 'Sent At', 'Message',  'Response', 'Response Updated At'), show='headings')
        responded_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Define column headings
        responded_tree.heading('Username', text='Username')
        responded_tree.heading('Email', text='Email')
        responded_tree.heading('Sent At', text='Sent At')
        responded_tree.heading('Message', text='Message')

        responded_tree.heading('Response', text='Response')
        responded_tree.heading('Response Updated At', text='Responsed By')

        for transfer in responded_transfers:
            # Mapping responded_id to corresponding email addresses
            responded_email = ''
            if transfer[6] == 1:
                responded_email = 'hr1@speakify.com'
            elif transfer[6] == 2:
                responded_email = 'hr2@speakify.com'
            
            # Insert each responded transfer data into the treeview
            responded_tree.insert('', 'end', values=(transfer[0], transfer[1], transfer[2], transfer[3],  transfer[5], responded_email,transfer[7]))

    responded_button = tk.Button(responded_window, text="Close", command=responded_window.destroy)
    responded_button.grid(row=0, column=0, pady=5, padx=5)

root = tk.Tk()
root.title("Welcome HR1")
root.config(bg="lightgray")  # Set background color

# Create a connection to the database
connect = db.create_connection()

# Display data_transfer table content
display_data_transfer(connect)

# Function for logging out
def logout():
    root.destroy()
    os.system("python login_ui.py") 
    
    # Call the logout function or perform any necessary logout actions

download_button = tk.Button(root, text="Download Report", command=lambda: download_report(connect), bg="green", fg="white")
download_button.grid(row=0, column=0, pady=5, padx=5)

viewResponded_button = tk.Button(root, text="View Responded Mails", command=display_responded_data, bg="black", fg="white")
viewResponded_button.grid(row=0, column=1, pady=5, padx=5)

logout_button = tk.Button(root, text="Logout", command=logout, bg="red", fg="white")
logout_button.grid(row=0, column=2, pady=5, padx=5)

root.mainloop()
