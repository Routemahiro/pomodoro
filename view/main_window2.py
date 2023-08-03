from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QProgressBar
from PySide6.QtGui import QFont, QColor, QPainter, QPen
from PySide6.QtCore import Qt

class CustomProgressBar(QProgressBar):
    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(12)
        pen.setColor(QColor("#BF3939"))
        painter.setPen(pen)
        painter.drawLine(0, 6, self.value() / 100 * self.width(), 6)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mikage_Timer")
        self.setStyleSheet("background-color: #F2F1DC;")
        self.setFixedSize(500, 300)
        self.setup_ui()

    def setup_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()


        # Element 1
        timer_label = QLabel("00:00")
        timer_label.setStyleSheet("color: #222222;")
        timer_label.setFont(QFont('x12y12pxMaruMinya', 50))
        # timer_label.setFixedHeight(100)  # Adjust the height based on the font size

        progress_bar = CustomProgressBar()
        progress_bar.setFixedSize(340, 12)

        start_button = QPushButton("Start")
        start_button.setStyleSheet("""
            background-color: #F2C438; 
            color: #222222; 
            border-radius: 14px;
            font-size: 30px;
        """)
        start_button.setFixedSize(340, 85)


        layout.addWidget(timer_label, alignment=Qt.AlignCenter)
        layout.addWidget(progress_bar, alignment=Qt.AlignCenter)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        # Element 2
        # Please note that actual circular buttons require more complex code, here I use simple QPushButton for simplicity
        dl_button = QPushButton("DL")
        dl_button.setStyleSheet("background-color: #FFFFFF; color: #222222; border-radius: 30px; font-size: 30px;")
        dl_button.setFixedSize(60, 60)

        settings_button = QPushButton("設定")
        settings_button.setStyleSheet("background-color: #FFFFFF; color: #222222; border-radius: 30px; font-size: 25px;")
        settings_button.setFixedSize(60, 60)

        layout.addWidget(dl_button, alignment=Qt.AlignRight)
        layout.addWidget(settings_button, alignment=Qt.AlignRight)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication([])
    font = QFont('x12y12pxMaruMinya', 14)
    app.setFont(font)
    window = MainWindow()
    window.show()
    app.exec_()
