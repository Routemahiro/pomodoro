from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QLCDNumber
from PySide6.QtCore import QTimer
import sys

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pomodoro Timer")
        self.setGeometry(400, 180, 570, 405)

        # Create a timer
        self.timer = QLCDNumber(self)
        self.timer.setDigitCount(5)  # 00:00

        # Create buttons
        self.start_button = QPushButton("Start", self)
        self.data_dl_button = QPushButton("", self)
        self.setting_button = QPushButton("", self)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.timer)
        layout.addWidget(self.start_button)
        layout.addWidget(self.data_dl_button)
        layout.addWidget(self.setting_button)

        # Set layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

def main():
    app = QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()
