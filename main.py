from view.main_window import MainWindow
from controller.timer_controller import TimerController
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    main_window = MainWindow(root)  # MainWindowのインスタンスを作成
    timer_controller = TimerController(main_window)  # TimerControllerにMainWindowのインスタンスを渡す
    main_window.run()
