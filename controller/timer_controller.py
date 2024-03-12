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
from utils.config import Config

openai.api_key = os.getenv('OPENAI_API_KEY')

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

        print("Timer class's start is called.")
        self.running = True
        self.thread = threading.Thread(target=self._start_event_loop)
        self.thread.daemon = True
        self.thread.start()

    def _start_event_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.run())
        loop.close()

    def stop(self):
        print("Timer class's stop is called.")
        self.running = False
        if self.thread is not None:
            if self.thread != threading.current_thread():
                self.thread.join()

    async def run(self):
        print(f"Callback is: {self.callback}")
        try:
            while self.running:
                print("In Timer's run method.")
                await asyncio.sleep(self.interval)

                if self.running:
                    print("Calling callback.")
                    await self.callback()
        except Exception as e:
            print(f"An exception occurred in Timer's run method: {e}")

class PomodoroTimer:
    def __init__(self, timer_controller, session_id, work_time, break_time, work_callback, break_callback, update_ui_callback):
        print("PomodoroTimer is initialized.")
        self.timer_controller = timer_controller
        self.session_id = session_id
        self.work_time = work_time
        self.break_time = break_time
        self.work_callback = work_callback
        self.break_callback = break_callback
        self.timer = Timer(1, self.update_timer)
        self.timer_session = PomodoroSession()
        self.work_mode = True
        self.update_ui_callback = update_ui_callback
        self.timer_paused = False
        self.remaining_time = self.work_time
        self.last_ai_comment = None
        self.pomodoro_id = 1
        self.timer_paused_lock = threading.Lock()

        self.db_handler = DBHandler()
        self.text_generator = TextGenerator()

    def start(self):
        print("PomodoroTimer's start is called.")
        self.timer.start()
        print("Timer's start is called.")

    def pause_timer(self):
        with self.timer_paused_lock:
            self.timer_paused = not self.timer_paused

    async def update_work_activity(self):
        if self.timer_paused:
            return

        try:
            print("update_work_activity is called")
            print(f"work_mode: {self.work_mode}")
            if not self.work_mode:
                return

            window_name = self.get_window_name()
            activity_genre = await self.estimate_activity_genre(window_name)
            current_time = datetime.now()

            self.db_handler.add_window_activity(self.pomodoro_id, self.session_id, current_time, window_name, activity_genre)
            self.update_ui_callback()
        except Exception as e:
            print(f"Error in update_work_activity: {e}")

    def stop(self):
        print("PomodoroTimer's stop is called.")
        self.timer.stop()

    async def update_timer(self):
        with self.timer_controller.timer_paused_lock:
            if self.timer_paused:
                print("Timer is paused in update_timer.")
                return

        if self.remaining_time > 0:
            self.remaining_time -= 1
            print("pomodorotimerクラスの残り時間" + str(self.remaining_time) + """\n
            """)
            if self.remaining_time % 60 == 0:
                await self.update_work_activity()
        else:
            await self.async_switch_mode()

    async def async_switch_mode(self):
        print("Async Switch_mode is called.")
        self.stop()
        if self.work_mode:
            self.remaining_time = self.break_time
            self.work_mode = False

            activities = self.db_handler.get_activities(self.session_id, self.pomodoro_id)
            self.pomodoro_id += 1

            messages = [
                {"role": "system", "content": "チャットAIです。会話します。"},
                {"role": "user", "content": f"私は以下の作業を行いました：{activities}"}
            ]

            ai_comment = await self.text_generator.generate_message(messages)
            self.last_ai_comment = ai_comment
            self.work_callback(ai_comment)
        else:
            self.remaining_time = self.work_time
            self.work_mode = True

            messages = [
                {"role": "system", "content": "チャットAIです。会話します。"},
                {"role": "user", "content": "休憩時間が終わりました"}
            ]

            ai_comment = await self.text_generator.generate_message(messages)
            self.last_ai_comment = ai_comment
            self.break_callback(ai_comment)

        self.update_ui_callback()

    def switch_mode(self):
        asyncio.run(self.async_switch_mode())

    def get_window_name(self):
        window = gw.getActiveWindow()

        if window is None:
            return "No Active Window"
        else:
            return window.title

    async def estimate_activity_genre(self, window_name):
        activity_genre = self.db_handler.get_activity_genre_by_window_name(window_name)

        if activity_genre:
            return activity_genre

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
            print(response)
            self.db_handler.add_activity_genre(window_name, response["choices"][0]["message"]["content"])
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error in estimate_activity_genre: {e}")
            return None

import json
from plyer import notification

class TimerController:
    def __init__(self, main_window):
        self.main_window = main_window
        config = Config()

        self.work_time = int(config.get("work_time")) * 60
        self.short_break_time = int(config.get("short_break_time")) * 60
        self.long_break_time = int(config.get("long_break_time")) * 60

        self.is_work_session = True
        self.session_count = 1
        self.timer_paused = False
        self.timer_paused_lock = threading.Lock()  # <- この行を追加
        self.update_ui_callback = self.update_ui
        self.pomodoro_timer = None
        self.db_handler = DBHandler()
        self.session_id = self.db_handler.create_session()

    def start_timer(self):
        if self.pomodoro_timer is None:
            self.pomodoro_timer = PomodoroTimer(self, self.session_id, self.work_time, self.short_break_time, self.work_callback, self.break_callback, self.update_ui_callback)
            self.pomodoro_timer.start()
        else:
            print("Timer is already running.")

    def pause_timer(self):
        if self.pomodoro_timer is not None:
            self.pomodoro_timer.pause_timer()
        else:
            print("No timer to pause.")

    def stop_timer(self):
        if self.pomodoro_timer is not None:
            self.pomodoro_timer.stop()
            self.pomodoro_timer = None
        else:
            print("No timer to stop.")

    def work_callback(self, ai_comment):
        notification_title = "作業が終了しました"
        notification_message = ai_comment
        notification.notify(title=notification_title, message=notification_message)

        if self.session_count < 4:
            self.pomodoro_timer = PomodoroTimer(self, self.session_id, self.work_time, self.short_break_time, self.work_callback, self.break_callback, self.update_ui_callback)
        else:
            self.pomodoro_timer = PomodoroTimer(self, self.session_id, self.work_time, self.long_break_time, self.work_callback, self.break_callback, self.update_ui_callback)
            self.session_count = 0

        self.session_count += 1
        self.is_work_session = False
        self.update_ui()
        self.pomodoro_timer.start()

    def break_callback(self, ai_comment):
        notification_title = "休憩が終了しました"
        notification_message = ai_comment
        notification.notify(title=notification_title, message=notification_message)

        self.pomodoro_timer = PomodoroTimer(self, self.session_id, self.work_time, self.short_break_time, self.work_callback, self.break_callback, self.update_ui_callback)
        self.is_work_session = True
        self.update_ui()
        self.pomodoro_timer.start()

    def update_ui(self):
        if self.pomodoro_timer is not None:
            remaining_time = self.pomodoro_timer.remaining_time
            minutes, seconds = divmod(remaining_time, 60)
            time_str = f"{minutes:02d}:{seconds:02d}"

            if self.is_work_session:
                status = "作業中"
            else:
                status = "休憩中"

            self.main_window.update_timer_display(time_str, status)
            self.main_window.update_ai_comment(self.pomodoro_timer.last_ai_comment)
        else:
            self.main_window.update_timer_display("25:00", "作業中")
            self.main_window.update_ai_comment(None)