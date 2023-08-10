#view/main_window.py
from tkinter import Tk, Canvas, Button, PhotoImage
from pathlib import Path
from view.settings_window import SettingsWindow  # 設定ウィンドウのクラスをインポート
import time
import json


OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "view" / "img" / "main"


class MainWindow:
    
    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def __init__(self, root):
        self.window = root
        self.window.geometry("500x300")
        self.window.configure(bg="#F2F1DC")
        # タイマーの開始時間を秒単位で設定（25分 = 1500秒）
        self.progress_bar_length = 381.0  # 最大長さを381.0に設定
        self.timer_seconds = 1500
    # キャンバスをインスタンス変数として保存
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

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        # 「おしまい」のボタン画像をロード
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))

        # スタートボタン
        self.button_start = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_timer,  # タイマーを開始するためのコマンド
            relief="flat"
        )
        self.button_start.place(x=37.0, y=185.0, width=344.0, height=85.0)

       



        # プログレスバーの最大長さを保存
        self.progress_bar_length = 341.0  # 最大長さを適切な値に設定

        # プログレスバーを作成し、そのIDを保存
        self.progress_bar = self.canvas.create_rectangle(
            40.0,
            144.0,
            40.0 + self.progress_bar_length,  # 最初は最大長さ
            156.0,
            fill="#BF3939",
            outline=""
        )

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
            command=self.open_settings,  # Updated command to open settings window
            relief="flat"
        )
        button_2.place(x=416.0, y=210.0, width=60.0, height=60.0)

        # 設定ファイルから時間を読み込む
        with open('utils/config.json', 'r') as file:
            config = json.load(file)
            self.work_time = int(config["work_time"]) * 60  # 分を秒に変換
            self.short_break_time = int(config["short_break_time"]) * 60
            self.long_break_time = int(config["long_break_time"]) * 60

        # タイマーの開始時間を作業時間に設定
        self.timer_seconds = self.work_time

        # セッションの状態とカウンターの初期化
        self.is_work_session = True  # 作業セッションかどうか
        self.session_count = 0  # セッションのカウント

        # 初期タイマーテキストを作業時間に基づいて設定
        initial_minutes, initial_seconds = divmod(self.work_time, 60)
        initial_time_str = f"{initial_minutes:02}:{initial_seconds:02}"
        self.initial_timer_text = self.canvas.create_text(
            114.0,
            32.0,
            anchor="nw",
            text=initial_time_str,
            fill="#222222",
            font=("x12y12pxMaruMinya", 80 * -1)
        )

        # タイマーのテキストを作成し、そのIDを保存
        self.timer_text = self.canvas.create_text(
            114.0,
            32.0,
            anchor="nw",
            text=initial_time_str,
            fill="#222222",
            font=("x12y12pxMaruMinya", 80 * -1)
        )

    def open_settings(self):  # New method to open settings window
        self.window.withdraw()  # メインウィンドウを非表示
        settings = SettingsWindow(self, self.window)  # self.windowを渡す
        settings.run()

    def show(self):  # 新しいメソッド
        self.window.deiconify()  # メインウィンドウを表示

    def start_timer(self):
        # スタートボタンの画像とコマンドを変更
        self.button_start.config(image=self.button_image_4, command=self.end_timer)

        # タイマーが開始されるときに、初期の "25:00" テキストを削除
        self.canvas.delete(self.initial_timer_text)
        self.remaining_time = self.timer_seconds


        # タイマーの時間をセッションに応じて設定
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

        self.update_timer()
        
    def update_timer(self):
        if self.remaining_time > 0:
            minutes, seconds = divmod(self.remaining_time, 60)
            time_str = f"{minutes:02}:{seconds:02}"
            self.canvas.itemconfig(self.timer_text, text=time_str)
            self.update_progress_bar(self.remaining_time)
            self.remaining_time -= 1
            self.window.after(1000, self.update_timer)
            
        if self.remaining_time <= 0:
            # セッションの切り替えとカウントの更新
            self.is_work_session = not self.is_work_session
            if not self.is_work_session:
                self.session_count += 1
            self.start_timer()

    def end_timer(self):
        # 「おしまい」ボタンがクリックされたときの処理
        # ここに後で追加する機能のコードを書く
        print("おしまいボタンがクリックされました")

    def update_progress_bar(self, remaining_time):
        progress_percentage = remaining_time / self.timer_seconds
        current_length = self.progress_bar_length * progress_percentage
        # 作業セッションと休憩セッションで色を切り替え
        fill_color = "#BF3939" if self.is_work_session else "#4E6BED"
        self.canvas.itemconfig(self.progress_bar, fill=fill_color)
        self.canvas.coords(self.progress_bar, 40.0, 144.0, 40.0 + current_length, 156.0)
         

    def run(self):
        self.window.mainloop()
