# main.py
# from view.main_window import MainWindow
# from tkinter import Tk

# if __name__ == "__main__":
#     root = Tk()
#     app = MainWindow(root)
#     app.run()

# main.py

from controller.timer_controller import TimerController
from view.main_window import MainWindow

if __name__ == "__main__":
    timer_controller = TimerController()
    main_window = MainWindow(timer_controller)
    main_window.run()
