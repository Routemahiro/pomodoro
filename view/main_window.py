#view/main_window.py
from tkinter import Tk, Canvas, Button, PhotoImage,Toplevel
from pathlib import Path
from view.settings_window import SettingsWindow  # 設定ウィンドウのクラスをインポート
from view.end_window import EndWindow
import time
import json



OUTPUT_PATH = Path.cwd()
ASSETS_PATH = OUTPUT_PATH / "view" / "img" / "main"


class MainWindow:
    
    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def __init__(self, root, controller=None):
        self.controller = controller
        print(f"Controller in MainWindow: {self.controller}")  # Debug
        self.window = root  # この行を変更
        self.window.geometry("500x300")
        self.window.configure(bg="#F2F1DC")
        self.progress_bar_length = 381.0
        self.timer_seconds = 1500
        self.progress_bar_color = "#BF3939" # プログレスバーの初期色
        self.timer_paused = False

        self.button_image_6 = PhotoImage(file=self.relative_to_assets("button_6.png"))

        # キャンバスの設定
        self.canvas = Canvas(self.window, bg="#F2F1DC", height=300, width=500, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # ボタン画像のロード
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))

        # スタートボタン
        self.button_start = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.start_timer, relief="flat")
        self.button_start.place(x=37.0, y=185.0, width=344.0, height=85.0)

        # プログレスバーの設定
        self.progress_bar_length = 341.0
        self.progress_bar = self.canvas.create_rectangle(40.0, 144.0, 40.0 + self.progress_bar_length, 156.0, fill="#BF3939", outline="")

        # その他のボタンの設定
        self.button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0, command=lambda: print("button_3 clicked"), relief="flat")
        self.button_3.place(x=416.0, y=144.0, width=60.0, height=60.0)
        self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.open_settings, relief="flat")
        self.button_2.place(x=416.0, y=210.0, width=60.0, height=60.0)

        # タイマー設定の読み込み
        with open('utils/config.json', 'r') as file:
            config = json.load(file)
            self.work_time = int(config["work_time"]) * 60
            self.short_break_time = int(config["short_break_time"]) * 60
            self.long_break_time = int(config["long_break_time"]) * 60
        self.timer_seconds = self.work_time
        self.is_work_session = True
        self.session_count = 0
        initial_minutes, initial_seconds = divmod(self.work_time, 60)
        initial_time_str = f"{initial_minutes:02}:{initial_seconds:02}"
        self.initial_timer_text = self.canvas.create_text(114.0, 32.0, anchor="nw", text=initial_time_str, fill="#222222", font=("x12y12pxMaruMinya", 80 * -1))
        self.timer_text = self.canvas.create_text(114.0, 32.0, anchor="nw", text=initial_time_str, fill="#222222", font=("x12y12pxMaruMinya", 80 * -1))

    def open_settings(self):  # New method to open settings window
        self.window.withdraw()  # メインウィンドウを非表示
        settings = SettingsWindow(self, self.window)  # self.windowを渡す
        settings.run()

    def show(self):  # 新しいメソッド
        self.window.deiconify()  # メインウィンドウを表示

    def set_controller(self, controller):
        self.controller = controller

    def start_timer(self):
        print(f"MainWindow's remaining_time: {self.controller.pomodoro_timer.remaining_time}")
        print(f"Controller in start_timer: {self.controller}")  # Debug
        print("start_timer is called")
        self.controller.start_timer()  # Modelにタイマーの開始を依頼

        # スタートボタンの画像とコマンドを変更
        self.button_start.config(image=self.button_image_4, command=self.end_timer)
        self.update_timer()

    def pause_timer(self):
        self.controller.pause_timer()  # TimerControllerに処理を委託


    def update_timer(self):
        self.controller.update_timer()  # TimerControllerに処理を委託
        remaining_time = self.controller.pomodoro_timer.remaining_time

        if remaining_time > 0:
            minutes, seconds = divmod(remaining_time, 60)
            time_str = f"{minutes:02}:{seconds:02}"
            print(time_str)
            self.canvas.itemconfig(self.timer_text, text=time_str)
            self.update_progress_bar(remaining_time)
            self.window.after(1000, self.update_timer)
        else:
            self.window.after(1000, self.start_timer)




    # MainWindow クラス内の end_timer メソッドの変更
    def end_timer(self):
        print("おしまいボタンがクリックされました")
        self.pause_timer()  # タイマーを一時停止
        EndQuestionWindow(self)  # 新しいウィンドウを表示

    def update_progress_bar(self, remaining_time):
        # タイマーが一時停止されていない場合、色を適切に設定
        if not self.timer_paused:
            self.progress_bar_color = "#BF3939" if self.is_work_session else "#4E6BED"

        progress_percentage = remaining_time / self.timer_seconds
        current_length = self.progress_bar_length * progress_percentage
        # 設定された色でプログレスバーを更新
        self.canvas.itemconfig(self.progress_bar, fill=self.progress_bar_color)
        self.canvas.coords(self.progress_bar, 40.0, 144.0, 40.0 + current_length, 156.0)


         

    def run(self):
        self.window.mainloop()



class EndQuestionWindow:
    ASSETS_PATH = Path.cwd() / "view" / "img" / "end_question"

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def __init__(self, parent):
        self.parent = parent  # 親ウィンドウへの参照を保持

        

        self.window = Toplevel(parent.window)
        self.window.geometry("300x200")
        self.window.configure(bg="#D9D9D9")
        self.window.resizable(False, False)
        # 以下の行を追加してウィンドウをモーダルにする
        self.window.grab_set()

        # Centering the window
        x = parent.window.winfo_x() + (parent.window.winfo_width() // 2) - (300 // 2)
        y = parent.window.winfo_y() + (parent.window.winfo_height() // 2) - (200 // 2)
        self.window.geometry("+%d+%d" % (x, y))

        canvas = Canvas(self.window, bg="#D9D9D9", height=200, width=300, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # button_1
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        # button_1 の command 属性の変更
        self.button_1 = Button(self.window, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.resume_timer, relief="flat")
        self.button_1.image = self.button_image_1
        self.button_1_window = canvas.create_window(0.0, 140.0, anchor="nw", window=self.button_1)


        # button_2
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        button_2 = Button(self.window, image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.open_end_window, relief="flat")
        button_2.image = self.button_image_2  # 画像への参照を保持
        button_2_window = canvas.create_window(150.0, 140.0, anchor="nw", window=button_2)

        canvas.create_text(11.0, 25.0, anchor="nw", text="きょうは\nおしまいにしますか？", fill="#222222", font=("x12y12pxMaruMinya", 20 * -1))

    # EndQuestionWindow クラスに resume_timer メソッドを追加
    def resume_timer(self):
        self.window.destroy()  # ウィンドウを閉じる
        self.parent.pause_timer()  # タイマーを再開


    def open_end_window(self):
        self.window.withdraw()  # 終了確認ウィンドウを非表示
        self.parent.window.withdraw()  # メインウィンドウを非表示
        end_window = EndWindow(self, self.window)  # self.windowを渡す
        end_window.run()