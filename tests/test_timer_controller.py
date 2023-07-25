import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.database import DBHandler, init_db
import sqlite3
from datetime import datetime

def test_get_activities():
    # テスト用のデータベースを初期化
    DB_PATH = 'model/database/test_mikage_timer.db'
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # テーブルを作成
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

    # テストデータを挿入
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO PomodoroSession (start_time)
        VALUES (?)
    ''', (start_time,))
    session_id = cursor.lastrowid

    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    window_name = "Test Window"
    cursor.execute('''
        INSERT INTO WindowActivity (session_id, time, window_name)
        VALUES (?, ?, ?)
    ''', (session_id, time, window_name))

    connection.commit()
    connection.close()

    # DBHandler を作成して get_activities を呼び出す
    db_handler = DBHandler(DB_PATH)
    activities = db_handler.get_activities(session_id)

    # 結果が期待したものと一致することを確認
    assert len(activities) == 1
    assert activities[0][1] == time
    assert activities[0][2] == window_name

if __name__ == "__main__":
    test_get_activities()
