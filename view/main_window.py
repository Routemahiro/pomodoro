# view\main_window.py
from tkinter import Tk, Canvas, Button, PhotoImage
from pathlib import Path
from view.settings_window import SettingsWindow  # 設定ウィンドウのクラスをインポート


OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "view" /"img"/  "main"




class MainWindow:

    def relative_to_assets(self, path: str) -> Path:  # selfを追加
        return ASSETS_PATH / Path(path)

    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x300")
        self.window.configure(bg="#F2F1DC")
        canvas = Canvas(
            self.window,
            bg = "#F2F1DC",
            height = 300,
            width = 500,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )



        canvas = Canvas(
            self.window,
            bg = "#F2F1DC",
            height = 300,
            width = 500,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))  # selfを追加
        button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=37.0,
            y=185.0,
            width=344.0,
            height=85.0
        )

        canvas.create_text(
            51.0,
            32.000000000000014,
            anchor="nw",
            text="25:00",
            fill="#222222",
            font=("x12y12pxMaruMinya", 80 * -1)
        )

        canvas.create_rectangle(
            40.0,
            144.0,
            381.0,
            156.0,
            fill="#BF3939",
            outline="")

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(x=416.0, y=210.0, width=60.0, height=60.0)

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        button_3.place(x=416.0, y=144.0, width=60.0, height=60.0)

            # Button to open settings window
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_settings,  # 更新されたコマンド
            relief="flat"
        )
        button_2.place(x=416.0, y=210.0, width=60.0, height=60.0)

    def open_settings(self):  # 設定ウィンドウを開くための新しいメソッド
        settings = SettingsWindow()
        settings.run()


    def run(self):
        self.window.mainloop()