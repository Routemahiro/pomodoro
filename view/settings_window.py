# view\seettings_window.py
"""設定画面でできること：ポモドーロセッションの作業時間や休憩時間の長さを設定"""
from pathlib import Path
from tkinter import Tk, Canvas, StringVar, OptionMenu, Button, PhotoImage
from utils.config import save_config


OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "view" / "img" / "setting"
options = [str(i) for i in range(1, 61)]  # Options for the dropdowns


class SettingsWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x300")
        self.window.configure(bg="#F2F1DC")

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

        self.var1 = StringVar(self.window)
        self.var1.set(options[24])  # default value
        entry_1 = OptionMenu(self.window, self.var1, *options)
        entry_1.place(x=319.0, y=24.0, width=144.0, height=29.0)

        self.var2 = StringVar(self.window)
        self.var2.set(options[4])  # default value
        entry_2 = OptionMenu(self.window, self.var2, *options)
        entry_2.place(x=320.0, y=86.0, width=144.0, height=29.0)

        self.var3 = StringVar(self.window)
        self.var3.set(options[14])  # default value
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

        # ... other widgets ...

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_settings,
            relief="flat"
        )
        self.button_1.place(x=340.0, y=215.0, width=140.0, height=57.0)

        # ... other widgets ...

    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def save_settings(self):
        work_time = self.var1.get()
        short_break_time = self.var2.get()
        long_break_time = self.var3.get()
        save_config(work_time, short_break_time, long_break_time)
        print("Settings saved!")

    def run(self):
        self.window.mainloop()
