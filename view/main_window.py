#view/main_window.py
from tkinter import Tk, Canvas, Button, PhotoImage,Toplevel, DISABLED, NORMAL
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

        # キャンバスの設定
        self.canvas = Canvas(self.window, bg="#F2F1DC", height=300, width=500, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # ボタン画像のロード
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_image_4_dark = PhotoImage(file=self.relative_to_assets("button_4_dark.png"))
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))
        self.button_image_6 = PhotoImage(file=self.relative_to_assets("button_6.png"))

        # スタートボタン
        self.button_start = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.start_timer, relief="flat")
        self.button_start.place(x=37.0, y=185.0, width=344.0, height=85.0)

        # プログレスバーの設定
        self.progress_bar_length = 341.0
        self.progress_bar = self.canvas.create_rectangle(40.0, 144.0, 40.0 + self.progress_bar_length, 156.0, fill="#BF3939", outline="")

        # その他のボタンの設定
        self.button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0, command=lambda: print("button_3 clicked"), relief="flat")
        self.button_3.place(x=416.0, y=144.0, width=60.0, height=70.0)
        self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.open_settings, relief="flat")
        self.button_2.place(x=416.0, y=210.0, width=60.0, height=70.0)

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
        # self.initial_timer_text = self.canvas.create_text(114.0, 32.0, anchor="nw", text=initial_time_str, fill="#222222", font=("x12y12pxMaruMinya", 80 * -1))
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
        print("start_timer is called")
        self.controller.start_timer()  # Modelにタイマーの開始を依頼

        # スタートボタンの画像とコマンドを変更
        self.button_start.config(image=self.button_image_4, command=self.end_timer)
        self.update_timer()

        # button_2とbutton_3を非表示にする
        self.button_2.place_forget()
        self.button_3.place_forget()
        # button_5をbutton_2の位置に表示する
        self.button_5 = Button(image=self.button_image_5, borderwidth=0, highlightthickness=0, command=self.pause_timer2, relief="flat")
        self.button_5.place(x=416.0, y=210.0, width=60.0, height=70.0)


    def pause_timer(self):
        self.controller.pause_timer()  # TimerControllerに処理を委託
        self.toggle_start_button()

    def pause_timer2(self):
        self.controller.pause_timer()  # TimerControllerに処理を委託

        # ウィンドウ左上に「一時停止中」と表示
        if 'pause_text' in self.__dict__:
            self.canvas.delete(self.pause_text)
            del self.pause_text
        else:
            self.pause_text = self.canvas.create_text(10, 10, anchor="nw", text="一時停止中", fill="#222222", font=("x12y12pxMaruMinya", 16))

        # button_5とbutton_6の表示を切り替える
        if 'button_6' in self.__dict__:
            self.button_6.place_forget()
            del self.button_6
            self.button_5.place(x=416.0, y=210.0, width=60.0, height=70.0)
        else:
            self.button_5.place_forget()
            self.button_6 = Button(image=self.button_image_6, borderwidth=0, highlightthickness=0, command=self.pause_timer2, relief="flat")
            self.button_6.place(x=416.0, y=210.0, width=60.0, height=70.0)

        self.toggle_start_button()

    def toggle_start_button(self):
        if self.button_start['state'] == NORMAL:
            self.button_start.config(image=self.button_image_4_dark, state=DISABLED)
        else:
            self.button_start.config(image=self.button_image_4, state=NORMAL, command=self.end_timer)


    def update_timer(self):
        self.controller.update_timer()  # TimerControllerに処理を委託
        remaining_time = self.controller.pomodoro_timer.remaining_time
        print(f"MainWindow's update_timer, remaining_time: {remaining_time}")  # Debug: この行を追加

        if remaining_time > 0:
            minutes, seconds = divmod(remaining_time, 60)
            time_str = f"{minutes:02}:{seconds:02}"
            print(time_str)
            self.canvas.itemconfig(self.timer_text, text=time_str)
            self.update_progress_bar(remaining_time)
            self.window.after(1000, self.update_timer)
        else:
            self.is_work_session = not self.is_work_session  # セッションの種類を切り替える
            self.window.after(1000, self.update_timer)  # こちらも再度update_timerを呼び出す




    # MainWindow クラス内の end_timer メソッドの変更
    def end_timer(self):
        print("おしまいボタンがクリックされました")
        self.controller.pause_timer()  # タイマーを一時停止
        EndQuestionWindow(self)  # 新しいウィンドウを表示

    def update_progress_bar(self, remaining_time):
        # この関数はメインスレッドで動作します
        def update_gui():
            # タイマーが一時停止されていない場合、色を適切に設定
            if not self.timer_paused:
                self.progress_bar_color = "#BF3939" if self.is_work_session else "#4E6BED"

            # 作業時間か休憩時間かに応じてtimer_secondsを更新
            self.timer_seconds = self.work_time if self.is_work_session else self.short_break_time

            progress_percentage = remaining_time / self.timer_seconds
            current_length = self.progress_bar_length * progress_percentage

            # 設定された色でプログレスバーを更新
            self.canvas.itemconfig(self.progress_bar, fill=self.progress_bar_color)
            self.canvas.coords(self.progress_bar, 40.0, 144.0, 40.0 + current_length, 156.0)

        # afterメソッドを使用してGUIの更新をスケジュールします
        self.window.after(0, update_gui)





         

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

        # button_1（こっちは続けるボタン）
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        # button_1 の command 属性の変更
        self.button_1 = Button(self.window, image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.resume_timer, relief="flat")
        self.button_1.image = self.button_image_1
        self.button_1_window = canvas.create_window(0.0, 140.0, anchor="nw", window=self.button_1)


        # button_2（こっちは終了ボタン）
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
