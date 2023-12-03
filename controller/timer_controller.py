# controller/timer_controller.py
from model.database import DBHandler
from utils.text_generator import TextGenerator
from model.pomodoro_session import PomodoroSession
import threading
import time
import asyncio
import aiohttp
import datetime
from datetime import datetime
import os
import openai
import pygetwindow as gw
from threading import Lock

openai.api_key = os.getenv('OPENAI_API_KEY')  # APIキーの設定を関数の外部に移動

class Timer:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.running = False
        self.thread = None

    def start(self):
        if self.thread is not None and self.thread.is_alive():
            print("Timer thread is already running!")
            return

        print("Timer class's start is called.")  # Debug
        self.running = True
        self.thread = threading.Thread(target=self._start_event_loop)
        self.thread.daemon = True  # Set the thread as a daemon
        self.thread.start()

    def _start_event_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run())
        loop.close()

    def stop(self):
        print("Timer class's run is started.")  # Debug
        self.running = False
        if self.thread is not None:
            self.thread.join()

    async def run(self):
        print(f"Callback is: {self.callback}")
        try:
            while self.running:
                print("In Timer's run method.")  # Debug
                await asyncio.sleep(self.interval)

                if self.running:
                    print("Calling callback.")  # Debug
                    await self.callback()
        except Exception as e:
            print(f"An exception occurred in Timer's run method: {e}")

class PomodoroTimer:
    def __init__(self, session_id, work_time, break_time, work_callback, break_callback,update_ui_callback):
        print("PomodoroTimer is initialized.")  # Debug
        self.cancel_timer = False
        self.session_id = session_id
        self.work_time = work_time
        self.break_time = break_time
        self.work_callback = work_callback
        self.break_callback = break_callback
        self.timer = Timer(1, self.update_timer)  # インターバルを1秒に設定
        self.lock = Lock()  # ロックを初期化
        self.timer_session = PomodoroSession()
        self.work_mode = True
        self.activity_timer = Timer(60, self.update_work_activity)  # 1分ごとにupdate_work_activityを呼び出すタイマー
        self.update_ui_callback = update_ui_callback  # UIを更新するためのコールバック
        self.timer_paused = False
        self.remaining_time = self.work_time
        self.last_ai_comment = None  # Add this line to initialize ai_comment
        self.pomodoro_id = 1  # ポモドーロIDを初期化



        # Create a DBHandler and TextGenerator instances
        self.db_handler = DBHandler()
        self.text_generator = TextGenerator()

    def start(self):
        print("PomodoroTimer's start is called.")  # Debug
        # self.timer.interval = 1
        self.timer.start()
        self.activity_timer.start()  # この行を追加
        print("Timer's start is called.")  # Debug

    def decrement_remaining_time(self):
        with self.lock:
            self.remaining_time -= 1

    def get_remaining_time(self):
        print(self.remaining_time)
        return self.remaining_time

    def is_timer_paused(self):
        return self.timer_paused

    async def update_work_activity(self):
        try:
            print("update_work_activity is called")  # 追加
            print(f"work_mode: {self.work_mode}")  # 追加
            if not self.work_mode:
                return

            # Get the current window name
            window_name = self.get_window_name()

            # Estimate the activity genre
            activity_genre = await self.estimate_activity_genre(window_name)


            # Get the current time
            current_time = datetime.now()

            # Add the window activity to the database
            self.db_handler.add_window_activity(self.pomodoro_id,self.session_id, current_time, window_name, activity_genre)

            self.update_ui_callback()  # UIを更新
        except Exception as e:
            print(f"Error in update_work_activity: {e}")
        




    def stop(self):
        print("PomodoroTimer's stop is called.")  # Debug
        self.timer.stop()
        self.activity_timer.stop()  # 活動タイマーを停止

    async def update_timer(self):
        print("update_timer called")  # デバッグログを追加
        with self.lock:  # ロックを取得
            if self.timer_paused or self.cancel_timer:
                return

            if self.remaining_time > 0:
                self.remaining_time -= 1
            else:
                await self.async_switch_mode()  # こちらを修正


    async def async_switch_mode(self):

        print("async_switch_mode called")  # デバッグログを追加
        with self.lock:
            print("Async Switch_mode is called.")  # Debug
            if self.work_mode:
                # Work time has ended
                self.remaining_time = self.break_time

                # Get work activities from the database
                activities = self.db_handler.get_activities(self.session_id, self.pomodoro_id)

                
                # 作業セッションが終わったので、新しいポモドーロIDを生成
                self.pomodoro_id += 1
                # Create a message for the AI
                messages = [
                    {"role": "system", "content": "チャットAIです。会話します。"},
                    {"role": "user", "content": f"私は以下の作業を行いました：{activities}"}
                ]

                # Get a comment from the AI
                ai_comment = await self.text_generator.generate_message(messages)
                self.last_ai_comment = ai_comment  # Save ai_comment here

                # Call the work callback with the AI comment
                self.work_callback(ai_comment)
                self.remaining_time = self.break_time
            else:
                # Break time has ended
                self.remaining_time = self.work_time

                # Create a message for the AI
                messages = [
                    {"role": "system", "content": "チャットAIです。会話します。"},
                    {"role": "user", "content": "休憩時間が終わりました"}
                ]

                # Get a comment from the AI
                ai_comment = await self.text_generator.generate_message(messages)
                self.last_ai_comment = ai_comment  # Save ai_comment here

                # Call the break callback with the AI comment
                self.break_callback(ai_comment)
                self.remaining_time = self.work_time

            self.work_mode = not self.work_mode
            self.update_ui_callback()  # UIを更新


    def switch_mode(self):
        asyncio.run(self.async_switch_mode())

    def get_window_name(self):
        # アクティブウィンドウの取得
        window = gw.getActiveWindow()

        # ウィンドウが見つからなかった場合のエラーハンドリング
        if window == None:
            return "No Active Window"
        else:
            return window.title


    async def estimate_activity_genre(self, window_name):
        # Check the database first
        activity_genre = self.db_handler.get_activity_genre_by_window_name(window_name)
        
        # If the genre is found in the database, return it without asking the AI
        if activity_genre:
            return activity_genre

        # Otherwise, ask the AI
        messages = [
            {"role": "system", "content": "あなたはユーザーの操作していたウィンドウ名から、作業ジャンルを一言で表す仕事を行います"},
            {"role": "user", "content": f"右にお送りするウィンドウ名から、作業ジャンルを一言で表してください {window_name}"}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0
            )
            print(response)  # レスポンスをログ出力
            # Store the response in the database for future reference
            self.db_handler.add_activity_genre(window_name, response["choices"][0]["message"]["content"])
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error in estimate_activity_genre: {e}")
            return None





# Main_windowから移動
import json
from plyer import notification
from threading import Lock


class TimerController:
    def __init__(self,main_window):
        self.main_window = main_window  # この行を追加
        self.load_config()
        self.timer_seconds = self.work_time
        self.is_work_session = True
        self.session_count = 0
        update_ui_callback=self.update_ui  # この行を追加
        self.lock = Lock()  # ロックを初期化



        # PomodoroTimer インスタンスを作成
    # PomodoroTimer インスタンスを作成
        db_handler = DBHandler()  # DBHandler インスタンスの作成
        last_session_id = db_handler.get_last_session_id()  # 最後のセッション ID を取得
        new_session_id = last_session_id + 1  # 新しいセッション ID

        self.pomodoro_timer = PomodoroTimer(session_id=new_session_id, work_time=self.work_time, break_time=self.short_break_time,
                                            work_callback=self.work_callback, break_callback=self.break_callback, update_ui_callback=self.update_ui)

        print("PomodoroTimer instance created in TimerController.")  # Debug

        self.main_window = main_window  # MainWindowのインスタンスを保持

    def load_config(self):
        with open('utils/config.json', 'r') as file:
            config = json.load(file)
            self.work_time = int(config["work_time"]) * 60
            self.short_break_time = int(config["short_break_time"]) * 60
            self.long_break_time = int(config["long_break_time"]) * 60
            # self.work_time = int(config["work_time"]) * 2
            # self.short_break_time = int(config["short_break_time"]) * 2
            # self.long_break_time = int(config["long_break_time"]) * 2

    def start_session(self):
        self.pomodoro_timer.db_handler.start_session()

    def end_session(self, ai_comment):
        self.db_handler.end_session(ai_comment)
    
    def work_callback(self, ai_comment):
        print("Work callback is called.")
        print(f"AI Comment: {ai_comment}")
        # titleの最大文字数は64
        # messageの最大文字数は256
        notification.notify(
            title='さぎょおわ',
            message=ai_comment,
            app_name='PomodoroApp',
            timeout=10
        )

    def break_callback(self, ai_comment):
        print("Break callback is called.")
        print(f"AI Comment: {ai_comment}")
        notification.notify(
            title='きゅけおわ',
            message=ai_comment,
            app_name='PomodoroApp',
            timeout=10
        )


    def start_timer(self):
        print("TimerController's start_timer is called")  # Debug
        self.start_session()  # Start a new session in the database
        self.pomodoro_timer.stop()
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
        self.pomodoro_timer.pause_timer()

    def end_timer(self):
        ai_comment = self.pomodoro_timer.last_ai_comment
        self.end_session(ai_comment)  # End the session in the database
        self.is_work_session = not self.is_work_session
        if not self.is_work_session:
            self.session_count += 1

    def update_timer(self):
        with self.lock:
            if self.pomodoro_timer.is_timer_paused() or self.cancel_timer:
                return

            remaining_time = self.pomodoro_timer.get_remaining_time()
            if remaining_time > 0:
                self.pomodoro_timer.decrement_remaining_time()
            else:
                self.is_work_session = not self.is_work_session
                if not self.is_work_session:
                    self.session_count += 1
                self.cancel_timer = True

    def update_ui(self):
        self.main_window.is_work_session = self.pomodoro_timer.work_mode
        remaining_time = self.pomodoro_timer.get_remaining_time()
        minutes, seconds = divmod(remaining_time, 60)
        time_str = f"{minutes:02}:{seconds:02}"
        self.main_window.update_timer_text(time_str)
        self.main_window.update_progress_bar(remaining_time)
        print("update_ui")