import tkinter as tk
from tkinter import ttk  # Correct import statement for ttk module
from datetime import datetime
import db
import tkinter.messagebox as tkmb

class MyMailsWindow(tk.Tk):
    def __init__(self, userid):
        super().__init__()
        self.userid = userid
        self.title("My Mail Window")

        self.geometry("500x500")  # Set window size

        # Create a Treeview widget to display data
        self.tree = ttk.Treeview(self, columns=('Username', 'Email', 'Sent At', 'Message', 'Data Transfer Status', 'Response Message', 'Responded', 'Response Updated At', 'Message Status'), show='headings')
        # Make sure the column names match the order of columns in your SQL query
        self.tree.heading('Username', text='Username')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Sent At', text='Sent At')
        self.tree.heading('Message', text='Message')
        self.tree.heading('Data Transfer Status', text='Data Transfer Status')
        self.tree.heading('Response Message', text='Response Message')
        self.tree.heading('Responded', text='Responded')
        self.tree.heading('Response Updated At', text='Response Updated At')
        self.tree.heading('Message Status', text='Message Status')
        
        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the Treeview and scrollbar widgets
        self.tree.pack(fill='both', expand=True, side="left")
        scrollbar.pack(fill="y", side="right")

        # Call the method to update the table view
        self.update_table_view()

    def update_table_view(self):
        try:
            # Fetch the data for the specific user from the database and display it in the table
            connect = db.create_connection()
            with connect:
                cursor = connect.cursor()
                cursor.execute("""
                    SELECT 
                        u.username, u.email, dt.sended_at, dt.message, dt.status AS data_transfer_status, 
                        m.message AS response_message, m.responded_id AS responded, m.updated_at AS response_updated_at, 
                        m.status AS message_status 
                    FROM 
                        users u 
                    JOIN 
                        data_transfer dt ON u.uid = dt.userid 
                    LEFT JOIN 
                        messages m ON dt.did = m.did 
                    WHERE 
                        u.uid = ?""", (self.userid,))
                transfers = cursor.fetchall()
                
                # Clear previous data in the table
                for record in self.tree.get_children():
                    self.tree.delete(record)
                
                # Insert fetched data into the table
                for transfer in transfers:
                    # Handle NULL values if any
                    transfer_data = [value if value is not None else "" for value in transfer]
                    self.tree.insert('', 'end', values=transfer_data)
        except Exception as e:
            # Handle exceptions, for instance, display an error message
            tkmb.showerror("Error", str(e))
