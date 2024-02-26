import sqlite3
import os

def create_database():
    # Check if the database file exists
    if not os.path.isfile('speakify.db'):
        conn = sqlite3.connect('speakify.db')
        c = conn.cursor()

        # Create user table
        c.execute('''
            CREATE TABLE users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Create data_transfer table
        c.execute('''
            CREATE TABLE data_transfer (
                did INTEGER PRIMARY KEY AUTOINCREMENT,
                userid INTEGER NOT NULL,
                sended_at TEXT NOT NULL,
                message TEXT NOT NULL,
                mode BOOLEAN DEFAULT 0,
                status BOOLEAN DEFAULT 0
            )
        ''')

        # Create messages table
        c.execute('''
            CREATE TABLE messages (
                mid INTEGER PRIMARY KEY AUTOINCREMENT,
                did INTEGER NOT NULL,
                responded_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                status BOOLEAN DEFAULT 0
            )
        ''')

        conn.commit()
        conn.close()
        print("Database created successfully.")
    else:
        print("Database already exists.")

create_database()


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('speakify.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn