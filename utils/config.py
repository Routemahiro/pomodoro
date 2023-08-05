import json
import os
from pathlib import Path

class Config:
    def __init__(self, config_file=Path(__file__).parent / "config.json"):
        self.config_file = config_file
        self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {
                "work_time": 25,     # Default work time in minutes
                "short_break": 5,    # Default short break time in minutes
                "long_break": 15     # Default long break time in minutes
            }
            self._save_config()

    def _save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.settings, f)

    def set(self, key, value):
        self.settings[key] = value
        self._save_config()

    def get(self, key):
        return self.settings.get(key, None)
