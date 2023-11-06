# model/database.py
import os
import sqlite3
from datetime import datetime

DB_DIR = 'model/database'
DB_PATH = os.path.join(DB_DIR, 'mikage_timer.db')

class DBHandler:
    def __init__(self, db_path=DB_PATH):
        self.connection = self.create_connection(db_path)
        self.session_id = None  # セッションIDを追加

    def get_activity_genre_by_window_name(self, window_name):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT activity_genre
            FROM ActivityGenre
            WHERE window_name = ?
        ''', (window_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def add_activity_genre(self, window_name, activity_genre):
        cursor = self.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO ActivityGenre (window_name, activity_genre)
                VALUES (?, ?)
                ON CONFLICT(window_name) DO UPDATE SET activity_genre = excluded.activity_genre;
            ''', (window_name, activity_genre))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding activity genre: {e}")
        
    def add_window_activity(self, session_id, time, window_name, activity_genre=None):
        cursor = self.connection.cursor()
        print(f"Adding window activity: session_id={session_id}, time={time}, window_name={window_name}, activity_genre={activity_genre}")  # Add this line
        try:
            cursor.execute('''
                INSERT INTO WindowActivity (session_id, time, window_name, activity_genre)
                VALUES (?, ?, ?, ?)
            ''', (session_id, time, window_name, activity_genre))
            self.connection.commit()
            print("Window activity added successfully.")  # Add this line
        except sqlite3.Error as e:
            print(f"Error adding window activity: {e}")  # Add this line


    def create_connection(self, db_path):
        connection = None
        try:
            connection = sqlite3.connect(db_path, check_same_thread=False)  # <- add this parameter
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        return connection
    
    def get_activities(self, session_id):
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT *
            FROM WindowActivity
            WHERE session_id = ?
        ''', (session_id,))
        activities = cursor.fetchall()
        return activities

    def start_session(self):
        cursor = self.connection.cursor()
        start_time = datetime.now()
        cursor.execute('''
            INSERT INTO PomodoroSession (start_time)
            VALUES (?)
        ''', (start_time,))
        self.connection.commit()
        self.session_id = cursor.lastrowid  # Get the ID of the new session
    
    def end_session(self, ai_comment):
        cursor = self.connection.cursor()
        end_time = datetime.datetime.now()
        cursor.execute('''
            UPDATE PomodoroSession
            SET end_time = ?, ai_comment = ?
            WHERE session_id = ?
        ''', (end_time, ai_comment, self.session_id))
        self.connection.commit()

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ActivityGenre (
            window_name TEXT PRIMARY KEY,
            activity_genre TEXT
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
