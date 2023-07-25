# controller/timer_controller.py
from model.database import DBHandler
from utils.text_generator import TextGenerator
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
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()

    def run(self):
        while self.running:
            time.sleep(self.interval)
            if self.running:
                self.callback()

class PomodoroTimer:
    def __init__(self, session_id, work_time, break_time, work_callback, break_callback):
        self.session_id = session_id
        self.work_time = work_time
        self.break_time = break_time
        self.work_callback = work_callback
        self.break_callback = break_callback
        self.timer = Timer(self.work_time, self.switch_mode)
        self.work_mode = True

        # Create a DBHandler and TextGenerator instances
        self.db_handler = DBHandler()
        self.text_generator = TextGenerator()

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def switch_mode(self):
        if self.work_mode:
            self.timer.interval = self.break_time
            self.work_callback()
        else:
            self.timer.interval = self.work_time
            self.break_callback()
        self.work_mode = not self.work_mode

    def switch_mode(self):
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
        self.work_mode = not self.work_mode


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