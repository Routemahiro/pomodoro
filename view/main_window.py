from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

import sys

class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300,300, 400, 200)
        self.setWindowTitle("Pomodoro Timer")

        self.timer_label = QLabel("00:00", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setFont(QFont('Arial', 50))

        self.start_button = QPushButton("Start", self)

        self.data_dl_button = QPushButton("", self)
        self.data_dl_button.setStyleSheet(
            "QPushButton {"
            "background-color: #ff6347;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 50px;"
            "border-color: beige;"
            "}"
        )
        self.data_dl_button.setFixedSize(100, 100)

        self.setting_button = QPushButton("", self)
        self.setting_button.setStyleSheet(
            "QPushButton {"
            "background-color: #ff6347;"
            "border-style: outset;"
            "border-width: 2px;"
            "border-radius: 50px;"
            "border-color: beige;"
            "}"
        )
        self.setting_button.setFixedSize(100, 100)

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_button)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.data_dl_button)
        button_layout.addWidget(self.setting_button)
        
        layout.addLayout(button_layout)

        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    sys.exit(app.exec())
    
if __name__ == '__main__':
    main()
