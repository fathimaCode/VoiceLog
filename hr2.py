import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tkmb
import db  
from datetime import datetime
import os
def open_response_window(did):
    def send_response():
        # Get the content from the text area
        response_content = response_text.get("1.0", "end-1c")  # Get the text from the text area
        hrid = 2
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

    send_button = tk.Button(response_window, text="Send", command=send_response)
    send_button.pack()

def display_data_transfer(connect):
    with connect:
        cursor = connect.cursor()

        # Fetch data_transfer entries
        cursor.execute("SELECT * FROM data_transfer where status = 0")
        transfers = cursor.fetchall()

        # Create a Treeview widget to display data
        tree = ttk.Treeview(root, columns=('userid', 'Sent At', 'Message', 'Data Transfer Status'), show='headings')
        tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")  # Make the tree expand in all directions

        # Define column headings
        tree.heading('userid', text='userid')
        tree.heading('Sent At', text='Sent At')
        tree.heading('Message', text='Message')
        tree.heading('Data Transfer Status', text='Data Transfer Status')

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
        scrollbar.grid(row=1, column=3, sticky="ns")

        # Configure Treeview to use vertical scrollbar
        tree.configure(yscrollcommand=scrollbar.set)

        for transfer in transfers:
            sended_at_datetime = datetime.strptime(transfer[2], "%Y-%m-%d %H:%M:%S")
            current_datetime = datetime.now()
            current_date = datetime.now().date()
            sended_at_date = sended_at_datetime.date()
            difference = (current_date - sended_at_date).days
            if difference > 0:
                # Insert each transfer data into the treeview
                tree.insert('', 'end', values=transfer[1:])

                # Create a response button for each transfer
                response_button = tk.Button(root, text="Response", command=lambda did=transfer[0]: open_response_window(did), bg="blue", fg="white")
                response_button.grid(row=2+len(transfers), column=0, pady=5)

def logout():
    root.destroy()
    os.system("python login_ui.py") 

root = tk.Tk()
root.title("Welcome HR2")

# Create a connection to the database
connect = db.create_connection()

# Display data_transfer table content
display_data_transfer(connect)

logout_button = tk.Button(root, text="Logout", command=logout)
logout_button.grid(row=0, column=0, pady=5, padx=5, sticky="w")

root.mainloop()
