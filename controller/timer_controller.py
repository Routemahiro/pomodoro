# controller/timer_controller.py
from model.database import DBHandler
from utils.text_generator import TextGenerator
from model.pomodoro_session import PomodoroSession
import threading
import time
import asyncio
import aiohttp
import datetime

class Timer:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.running = False
        self.thread = None

    def start(self):
        print("Timer class's start is called.")  # Debug
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # Set the thread as a daemon
        self.thread.start()

    def stop(self):
        print("Timer class's run is started.")  # Debug
        self.running = False
        if self.thread is not None:
            self.thread.join()

    def run(self):
        print("In Timer's run method.")  # Debug
        try:
            while self.running:
                print("In Timer's run method.")  # Debug
                time.sleep(self.interval)

                if self.running:
                    print("Calling callback.")  # Debug
                    self.callback()
        except Exception as e:
            print(f"An exception occurred in Timer's run method: {e}")

class PomodoroTimer:
    def __init__(self, session_id, work_time, break_time, work_callback, break_callback,update_ui_callback):
        print("PomodoroTimer is initialized.")  # Debug
        self.session_id = session_id
        self.work_time = work_time
        self.break_time = break_time
        self.work_callback = work_callback
        self.break_callback = break_callback
        self.timer = Timer(self.work_time, self.switch_mode)
        self.timer_session = PomodoroSession()
        self.work_mode = True
        self.activity_timer = Timer(60, self.update_work_activity)  # 1分ごとにupdate_work_activityを呼び出すタイマー
        self.update_ui_callback = update_ui_callback  # UIを更新するためのコールバック
        self.timer_paused = False
        self.remaining_time = self.work_time


        # Create a DBHandler and TextGenerator instances
        self.db_handler = DBHandler()
        self.text_generator = TextGenerator()

    def start(self):
        # self.remaining_time = self.total_time
        print("PomodoroTimer's start is called.")  # Debug
        self.timer = Timer(1, self.update_timer)  # 1秒ごとにupdate_timerを呼び出す
        print("Timer's start is called.")  # Debug

    def stop(self):
        print("PomodoroTimer's stop is called.")  # Debug
        self.timer.stop()
        self.activity_timer.stop()  # 活動タイマーを停止

    def update_timer(self):
        print(f"TimerController's remaining_time: {self.remaining_time}")
        if self.remaining_time > 0:
            self.remaining_time -= 1
            if self.remaining_time == 0:
                self.switch_mode()
        else:
            # ここで他の必要な処理を実装する
            pass


    def switch_mode(self):
        print("Switch_mode is called.")  # Debug
        if self.work_mode:
            # Work time has ended
            self.timer.interval = self.break_time

            # Get work activities from the database
            activities = self.db_handler.get_activities(self.session_id)

            # Create a message for the AI
            messages = [
                {"role": "system", "content": "チャットAIです。会話します。"},
                {"role": "user", "content": f"私は以下の作業を行いました：{activities}"}
            ]

            # Get a comment from the AI
            ai_comment = self.text_generator.generate_message(messages)

            # Call the work callback with the AI comment
            self.work_callback(ai_comment)
            self.remaining_time = self.break_time
        else:
            # Break time has ended
            self.timer.interval = self.work_time

            # Create a message for the AI
            messages = [
                {"role": "system", "content": "チャットAIです。会話します。"},
                {"role": "user", "content": "休憩時間が終わりました"}
            ]

            # Get a comment from the AI
            ai_comment = self.text_generator.generate_message(messages)

            # Call the break callback with the AI comment
            self.break_callback(ai_comment)
            self.remaining_time = self.work_time
        self.work_mode = not self.work_mode
        self.update_ui_callback()  # UIを更新


    def update_work_activity(self):
        if not self.work_mode:
            return

        # Get the current window name
        window_name = self.get_window_name()

        # Estimate the activity genre
        activity_genre = self.estimate_activity_genre(window_name)

        # Get the current time
        current_time = datetime.now()

        # Add the window activity to the database
        self.db_handler.add_window_activity(self.session_id, current_time, window_name, activity_genre)

        self.update_ui_callback()  # UIを更新

    def get_window_name(self):
        # Implement the method to get the current window name
        pass

    def estimate_activity_genre(self, window_name):
        # Implement the method to estimate the activity genre from the window name
        pass

    async def estimate_activity_genre(self, window_name):
        # Create a message for the AI
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"What kind of activity do you think the user is doing based on this window name? {window_name}"}
        ]

        # Send a request to the AI
        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.openai.com/v1/engines/davinci/completions', json={
                'messages': messages,
                'max_tokens': 60
            }) as response:
                result = await response.json()
                return result['choices'][0]['message']['content']
            
        # 非同期処理によって、AIにジャンルの推定をしてもらう
        activity_genre = asyncio.run(self.estimate_activity_genre(window_name))





# Main_windowから移動
import json

class TimerController:
    def __init__(self,main_window):
        self.main_window = main_window  # この行を追加
        self.load_config()
        self.timer_seconds = self.work_time
        self.is_work_session = True
        self.session_count = 0
        self.timer_paused = False
        self.remaining_time = self.work_time  # 追加
        update_ui_callback=self.update_ui  # この行を追加



        # PomodoroTimer インスタンスを作成
        self.pomodoro_timer = PomodoroTimer(session_id=1, work_time=self.work_time, break_time=self.short_break_time,
                                            work_callback=self.work_callback, break_callback=self.break_callback,update_ui_callback=self.update_ui)
        print("PomodoroTimer instance created in TimerController.")  # Debug

        self.main_window = main_window  # MainWindowのインスタンスを保持

    def load_config(self):
        with open('utils/config.json', 'r') as file:
            config = json.load(file)
            self.work_time = int(config["work_time"]) * 60
            self.short_break_time = int(config["short_break_time"]) * 60
            self.long_break_time = int(config["long_break_time"]) * 60
    
    def work_callback(self, ai_comment):
        print("Work callback is called.")
        print(f"AI Comment: {ai_comment}")

    def break_callback(self, ai_comment):
        print("Break callback is called.")
        print(f"AI Comment: {ai_comment}")


    def start_timer(self):
        print("TimerController's start_timer is called")  # Debug
        self.pomodoro_timer.start()

        self.cancel_timer = False  # タイマーのキャンセルフラグをリセット

        # タイマーの時間をセッションに応じて設定
        if self.is_work_session:
            self.timer_seconds = self.work_time
        else:
            if self.session_count % 4 == 0:
                self.timer_seconds = self.long_break_time
            else:
                self.timer_seconds = self.short_break_time


    def pause_timer(self):
        self.timer_paused = not self.timer_paused

    def end_timer(self):
        self.is_work_session = not self.is_work_session
        if not self.is_work_session:
            self.session_count += 1

    def update_timer(self):
        if self.timer_paused or self.cancel_timer:
            return

        if self.remaining_time > 0:
            self.remaining_time -= 1
        else:
            self.is_work_session = not self.is_work_session
            if not self.is_work_session:
                self.session_count += 1
            self.cancel_timer = True

    def update_ui(self):
        # ここでUIの時間表示を更新するコードを書く
        print("A")