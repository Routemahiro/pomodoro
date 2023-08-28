from controller.timer_controller import TimerController
from view.main_window import MainWindow
from view.settings_window import SettingsWindow  # 既存の設定ウィンドウ
from view.end_window import EndWindow  # 既存の終了ウィンドウ

class WindowController:
    def __init__(self):
        self.timer_controller = TimerController()
        self.main_window = MainWindow(self)

    def start_timer(self):
        self.timer_controller.start_timer()
        self.main_window.update_view()

    def pause_timer(self):
        self.timer_controller.pause_timer()
        self.main_window.update_view()

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.run()

    def open_end_window(self):
        end_window = EndWindow(self)
        end_window.run()

    def update_view(self):
        self.main_window.update_view()
