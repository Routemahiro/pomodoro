import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import time
# tests/test_timer_controller.py
from controller.timer_controller import PomodoroTimer
# from utils.text_generator import generate_ai_text

def dummy_work_callback():
    # ダミーデータを作成
    dummy_data = [
        {"作業内容": "数学の勉強", "作業分数": "30分", "作業ジャンル": "学習"},
        {"作業内容": "コードの記述", "作業分数": "45分", "作業ジャンル": "仕事"},
    ]
    # ダミーデータを元に作業内容を作成
    work_done = ", ".join([f"{item['作業内容']}（{item['作業ジャンル']}）の作業分数は{item['作業分数']}" for item in dummy_data])
    return work_done

def dummy_break_callback():
    print("It's break time! Relax a bit!")

def test_timer_controller():
    pomodoro_timer = PomodoroTimer(25, 5, dummy_work_callback, dummy_break_callback)
    pomodoro_timer.start()
    time.sleep(30)  # Wait for 30 seconds to let the timer tick
    pomodoro_timer.stop()

if __name__ == "__main__":
    test_timer_controller()
