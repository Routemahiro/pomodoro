# database.py
import os
import sqlite3
from datetime import datetime

DB_DIR = 'model/database'
DB_PATH = os.path.join(DB_DIR, 'mikage_timer.db')

class DBHandler:
    def __init__(self):
        self.connection = self.create_connection()
        
    def add_window_activity(self, session_id, time, window_name):
        cursor = self.connection.cursor()

        cursor.execute('''
            INSERT INTO WindowActivity (session_id, time, window_name)
            VALUES (?, ?, ?)
        ''', (session_id, time, window_name))

        self.connection.commit()

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(DB_PATH)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return connection

    def start_pomodoro_session(self, start_time):
        cursor = self.connection.cursor()

        cursor.execute('''
            INSERT INTO PomodoroSession (start_time)
            VALUES (?)
        ''', (start_time,))

        self.connection.commit()
        session_id = cursor.lastrowid

        return session_id

    def end_pomodoro_session(self, session_id, end_time, ai_comment):
        cursor = self.connection.cursor()

        cursor.execute('''
            UPDATE PomodoroSession 
            SET end_time = ?, ai_comment = ? 
            WHERE session_id = ?
        ''', (end_time, ai_comment, session_id))

        self.connection.commit()

    def get_activity_duration(self, session_id):
        cursor = self.connection.cursor()

        cursor.execute('''
            SELECT min(time), max(time)
            FROM WindowActivity
            WHERE session_id = ?
        ''', (session_id,))

        start_time, end_time = cursor.fetchone()

        # Convert datetime strings to datetime objects
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        # Return the difference in minutes
        return int((end_time - start_time).total_seconds() / 60)
    
    def close_connection(self):
        if self.connection:
            self.connection.close()

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
