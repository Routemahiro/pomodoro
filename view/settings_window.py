# view\settings_window.py
import json
from pathlib import Path
from tkinter import Tk, Canvas, StringVar, OptionMenu, Button, PhotoImage,Toplevel
from utils.config import save_config
from view.settings_saved_window import SettingsSavedWindow

OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "view" / "img" / "setting"
options = [str(i) for i in range(1, 61)]  # Options for the dropdowns

class SettingsWindow:

    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    def __init__(self,main_window,root):
        self.window = Toplevel(root)  # Toplevelウィンドウを作成
        self.window.geometry("500x300")
        self.window.configure(bg="#F2F1DC")
        self.main_window = main_window # 追加
        canvas = Canvas(
            self.window,
            bg="#F2F1DC",
            height=300,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)

        # Load settings from config.json
        with open(Path("utils/config.json"), "r") as f:
            config = json.load(f)

        work_time = str(config["work_time"])
        short_break_time = str(config["short_break_time"])
        long_break_time = str(config["long_break_time"])

        self.var1 = StringVar(self.window)
        self.var1.set(work_time if work_time in options else options[24])  # default value
        entry_1 = OptionMenu(self.window, self.var1, *options)
        entry_1.place(x=319.0, y=24.0, width=144.0, height=29.0)

        self.var2 = StringVar(self.window)
        self.var2.set(short_break_time if short_break_time in options else options[4])  # default value
        entry_2 = OptionMenu(self.window, self.var2, *options)
        entry_2.place(x=320.0, y=86.0, width=144.0, height=29.0)

        self.var3 = StringVar(self.window)
        self.var3.set(long_break_time if long_break_time in options else options[14])  # default value
        entry_3 = OptionMenu(self.window, self.var3, *options)
        entry_3.place(x=319.0, y=149.0, width=144.0, height=29.0)

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = canvas.create_image(83.0, 149.0, image=self.image_image_1)

        canvas.create_text(
            161.0,
            23.0,
            anchor="nw",
            text="作業時間",
            fill="#222222",
            font=("x12y12pxMaruMinya", 20 * -1)
        )

        canvas.create_rectangle(
            161.0,
            62.0,
            480.0,
            65.0,
            fill="#BF3939",
            outline=""
        )

        canvas.create_text(
            161.0,
            85.0,
            anchor="nw",
            text="休憩時間（短）",
            fill="#222222",
            font=("x12y12pxMaruMinya", 20 * -1)
        )

        canvas.create_rectangle(
            161.0,
            124.0,
            463.0,
            127.0,
            fill="#4E6BED",
            outline=""
        )

        canvas.create_text(
            161.0,
            147.0,
            anchor="nw",
            text="休憩時間（長）",
            fill="#222222",
            font=("x12y12pxMaruMinya", 20 * -1)
        )

        canvas.create_rectangle(
            161.0,
            186.0,
            480.0,
            189.0,
            fill="#4E6BED",
            outline=""
        )

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.window,  # 親ウィジェットとしてToplevelウィンドウを指定
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_settings,
            relief="flat"
        )
        self.button_1.place(x=340.0, y=215.0, width=140.0, height=57.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.window,  # 親ウィジェットとしてToplevelウィンドウを指定
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.go_back_to_main,
            relief="flat"
        )
        self.button_2.place(
            x=176.0,
            y=223.0,
            width=108.0,
            height=45.0
        )

    def save_settings(self):
        work_time = self.var1.get()
        short_break_time = self.var2.get()
        long_break_time = self.var3.get()
        save_config(work_time, short_break_time, long_break_time)  # この行を修正
        print("Settings saved!")

    def go_back_to_main(self):
        SettingsSavedWindow(self.main_window)  # 設定保存ウィンドウを表示
        self.window.withdraw()  # 設定ウィンドウを一時的に隠す

    def run(self):
        self.window.mainloop()
