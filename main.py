# main.py
from view.main_window import MainWindow
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(root)
    app.run()