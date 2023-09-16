from view.main_window import MainWindow
from controller.timer_controller import TimerController
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    main_window = MainWindow(root)  # まずMainWindowのインスタンスを作成
    timer_controller = TimerController(main_window)  # main_windowを引数として渡す
    main_window.set_controller(timer_controller)  # MainWindowにTimerControllerのインスタンスをセット
    main_window.run()  