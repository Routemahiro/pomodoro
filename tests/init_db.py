#init_db.py
import os
import sqlite3

DB_DIR = 'tests/data'
DB_PATH = os.path.join(DB_DIR, 'mikage_timer.db')

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




# if __name__ == "__main__":
#     # Check if database directory exists, create it if not
#     if not os.path.isdir(DB_DIR):
#         os.mkdir(DB_DIR)
#     # Check if database file exists, initialize DB if not
#     if not os.path.isfile(DB_PATH):
#         init_db()
