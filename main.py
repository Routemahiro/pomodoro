# main.py
# from view.main_window import MainWindow
# from tkinter import Tk

# if __name__ == "__main__":
#     root = Tk()
#     app = MainWindow(root)
#     app.run()

from controller.window_controller import WindowController

if __name__ == "__main__":
    controller = WindowController()
    controller.main_window.run()