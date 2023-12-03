from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Toplevel, Button


OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "view" / "img" / "end"


class EndWindow:
    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def __init__(self, main_window,root):
        self.window = Toplevel(root)  # Toplevelウィンドウを作成
        self.window.geometry("500x300")
        self.window.configure(bg="#F2F1DC")
        self.window.resizable(False, False)
        self.main_window = main_window # 追加

        self.canvas = Canvas(
            self.window,
            bg="#F2F1DC",
            height=300,
            width=500,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            86.0,
            144.0,
            image=self.image_image_1
        )

        self.canvas.create_text(
            182.0,
            23.0,
            anchor="nw",
            text="おつかれさま\n\n今日はすごい\nデザインがんばってたね\n\n待ってるから、\nまた会いに来てよ",
            fill="#000000",
            font=("x12y12pxMaruMinya", 25 * -1)
        )

        # 画像を読み込む
        self.close_image = PhotoImage(file=self.relative_to_assets("close.png"))

        # ボタンを作成し、画像を設定
        self.close_button = Button(self.window, image=self.close_image, command=self.quit_program)

        # ボタンをCanvasに配置
        self.canvas.create_window(250, 250, window=self.close_button)

    def quit_program(self):
        # プログラムを終了する
        self.window.quit()

    def run(self):
        self.window.mainloop()
