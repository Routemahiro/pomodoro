# database.py
import os
import sqlite3
from datetime import datetime

DB_DIR = 'model/database'
DB_PATH = os.path.join(DB_DIR, 'mikage_timer.db')

class DBHandler:
    def __init__(self, db_path=DB_PATH):
        self.connection = self.create_connection(db_path)
        self.session_id = None  # セッションIDを追加
        
    def add_window_activity(self, session_id, time, window_name, activity_genre=None):
        cursor = self.connection.cursor()

        cursor.execute('''
            INSERT INTO WindowActivity (session_id, time, window_name, activity_genre)
            VALUES (?, ?, ?, ?)
        ''', (session_id, time, window_name, activity_genre))

        self.connection.commit()

    # Other methods are the same...

def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PomodoroSession (
            session_id INTEGER PRIMARY KEY,
            start_time DATETIME NOT NULL,
            end_time DATETIME,
            ai_comment TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WindowActivity (
            session_id INTEGER,
            time DATETIME NOT NULL,
            window_name TEXT NOT NULL,
            activity_genre TEXT,
            FOREIGN KEY(session_id) REFERENCES PomodoroSession(session_id)
        )
    ''')

    connection.commit()
    connection.close()

# Check if database directory exists, create it if not
if not os.path.isdir(DB_DIR):
    os.mkdir(DB_DIR)
# Check if database file exists, initialize DB if not
if not os.path.isfile(DB_PATH):
    init_db()
