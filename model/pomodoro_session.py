# model/pomodoro_session.py

import json
import time

class PomodoroSession:
    def __init__(self):
        with open('utils/config.json', 'r') as file:
            config = json.load(file)
            self.work_time = int(config["work_time"]) * 60
            self.short_break_time = int(config["short_break_time"]) * 60
            self.long_break_time = int(config["long_break_time"]) * 60

        self.timer_seconds = self.work_time
        self.remaining_time = self.timer_seconds
        self.is_work_session = True
        self.session_count = 0
        self.timer_paused = False
        self.cancel_timer = False

    def start_timer(self):
        self.cancel_timer = False
        self.timer_paused = False

        if self.is_work_session:
            self.remaining_time = self.work_time
            self.timer_seconds = self.work_time
        else:
            if self.session_count % 4 == 0:
                self.remaining_time = self.long_break_time
                self.timer_seconds = self.long_break_time
            else:
                self.remaining_time = self.short_break_time
                self.timer_seconds = self.short_break_time

    def pause_timer(self):
        self.timer_paused = not self.timer_paused

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

    def reset_timer(self):
        self.cancel_timer = True
        self.remaining_time = self.timer_seconds
