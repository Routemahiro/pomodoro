# tests/test_database.py
import os
import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.database import DBHandler, init_db

def test_database():
    # データベース初期化
    init_db()

    # DBHandlerのインスタンスを作成
    db_handler = DBHandler()

    # 新しいポモドーロセッションの開始
    start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session_id = db_handler.start_pomodoro_session(start_time)
    assert session_id is not None, "Failed to start a new pomodoro session."

    # 偽のウィンドウ活動を追加
    window_name = "dummy_window"
    db_handler.add_window_activity(session_id, start_time, window_name)

    # ポモドーロセッションの終了
    end_time = datetime.datetime.now()
    ai_comment = "Good job!"
    db_handler.end_pomodoro_session(session_id, end_time, ai_comment)

    # 活動期間の取得
    duration = db_handler.get_activity_duration(session_id)

    # データベース接続のクローズ
    db_handler.close_connection()

    print("All tests passed.")

if __name__ == "__main__":
    test_database()
