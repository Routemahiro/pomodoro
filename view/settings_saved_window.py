# view/settings_saved_window.py
from pathlib import Path
from tkinter import Toplevel, Canvas, PhotoImage

OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "view" / "img" / "setting_save"

class SettingsSavedWindow:
    def __init__(self, main_window):
        self.main_window = main_window  # 追加
        self.window = Toplevel(main_window.window)
        self.window.geometry("500x300")
        self.window.configure(bg="#AFAFAF")

        canvas = Canvas(
            self.window,
            bg="#AFAFAF",
            height=300,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        image_width = self.image_image_1.width()
        image_height = self.image_image_1.height()
        self.image_1 = canvas.create_image(image_width/2, image_height/2, image=self.image_image_1)


        canvas.create_text(
            165.0,
            242.0,
            anchor="nw",
            text="画面が閉じるまで",
            fill="#000000",
            font=("x12y12pxMaruMinya", 20 * -1)
        )

        # ここに他の画像やテキストを配置するコードを追加します。
        canvas.create_text(
            45.0,
            123.0,
            anchor="nw",
            text="休憩時間（短）：",
            fill="#000000",
            font=("x12y12pxMaruMinya", 28 * -1)
        )

        canvas.create_text(
            45.0,
            85.0,
            anchor="nw",
            text="作業時間　　　：",
            fill="#000000",
            font=("x12y12pxMaruMinya", 28 * -1)
        )

        canvas.create_text(
            45.0,
            161.0,
            anchor="nw",
            text="休憩時間（長）：",
            fill="#000000",
            font=("x12y12pxMaruMinya", 28 * -1)
        )

        canvas.create_text(
            296.0,
            161.0,
            anchor="nw",
            text="15分",
            fill="#000000",
            font=("x12y12pxMaruMinya", 28 * -1)
        )

        canvas.create_text(
            296.0,
            123.0,
            anchor="nw",
            text="5分",
            fill="#000000",
            font=("x12y12pxMaruMinya", 28 * -1)
        )

        canvas.create_text(
            296.0,
            85.0,
            anchor="nw",
            text="25分",
            fill="#000000",
            font=("x12y12pxMaruMinya", 28 * -1)
        )

        self.window.after(3000, self.go_back_to_main)  # 3秒後にメインウィンドウを再表示

    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def go_back_to_main(self):
        self.window.destroy()  # 設定保存ウィンドウを閉じる
        self.main_window.show()  # メインウィンドウを再表示
