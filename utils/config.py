import json
import os
from pathlib import Path

CONFIG_FILE = Path("utils/config.json")

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def save_config(work_time, short_break_time, long_break_time):
    config = {
        "work_time": work_time,
        "short_break_time": short_break_time,
        "long_break_time": long_break_time
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
# Config保存後にプログラムの再起動か、メインウィンドウの再起動を行いたい。現在だと設定変更したものが、すぐに反映されないので

class Config:
    def __init__(self, config_file=Path(__file__).parent / "config.json"):
        self.config_file = config_file
        self._load_config()

    def load_config():
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return None

    def save_config(work_time, short_break_time, long_break_time):
        config = {
            "work_time": work_time,
            "short_break_time": short_break_time,
            "long_break_time": long_break_time
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    def set(self, key, value):
        self.settings[key] = value
        self._save_config()

    def get(self, key):
        return self.settings.get(key, None)
