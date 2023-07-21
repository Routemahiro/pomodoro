#db_handler.py
import sqlite3
import os
from datetime import datetime


DB_DIR = 'database/data'
DB_PATH = os.path.join(DB_DIR, 'mikage_timer.db')



# class DBHandler:
#     def __init__(self):
#         self.connection = self.create_connection()

#     def create_connection(self):
#         connection = None
#         try:
#             connection = sqlite3.connect(DB_PATH)
#         except sqlite3.Error as e:
#             print(f"Error connecting to database: {e}")
#         return connection
    
# def create_connection():
#     connection = None
#     try:
#         connection = sqlite3.connect(DB_PATH)
#     except sqlite3.Error as e:
#         print(f"Error connecting to database: {e}")

#     return connection

# def start_pomodoro_session(start_time):
#     connection = create_connection()
#     cursor = connection.cursor()

#     cursor.execute('''
#         INSERT INTO PomodoroSession (start_time)
#         VALUES (?)
#     ''', (start_time,))

#     connection.commit()
#     session_id = cursor.lastrowid
#     connection.close()

#     return session_id

# def end_pomodoro_session(session_id, end_time, ai_comment):
#     connection = create_connection()
#     cursor = connection.cursor()

#     cursor.execute('''
#         UPDATE PomodoroSession 
#         SET end_time = ?, ai_comment = ? 
#         WHERE session_id = ?
#     ''', (end_time, ai_comment, session_id))

#     connection.commit()
#     connection.close()

# def get_activity_duration(session_id):
#     connection = create_connection()
#     cursor = connection.cursor()

#     cursor.execute('''
#         SELECT min(time), max(time)
#         FROM WindowActivity
#         WHERE session_id = ?
#     ''', (session_id,))

#     start_time, end_time = cursor.fetchone()
#     connection.close()

#     # Convert datetime strings to datetime objects
#     start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
#     end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

#     # Return the difference in minutes
#     return int((end_time - start_time).total_seconds() / 60)

class DBHandler:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

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