from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QComboBox, QFrame
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt

class SettingsWindow(QMainWindow):
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
        image_label = QLabel()
        pixmap = QPixmap('image.png')
        image_label.setPixmap(pixmap.scaled(200, 300, Qt.KeepAspectRatio))

        # Element 2
        work_time_label = QLabel("作業時間")
        work_time_combo = QComboBox()

        short_break_label = QLabel("休憩時間（短）")
        short_break_combo = QComboBox()

        long_break_label = QLabel("休憩時間（長）")
        long_break_combo = QComboBox()

        red_line = QFrame()
        red_line.setFrameShape(QFrame.HLine)
        red_line.setStyleSheet("background-color: #BF3939;")

        blue_line = QFrame()
        blue_line.setFrameShape(QFrame.HLine)
        blue_line.setStyleSheet("background-color: #4E6BED;")

        back_button = QPushButton("戻る")
        back_button.setStyleSheet("background-color: #A3A3A3; border-radius: 14px;")
        back_button.setFixedSize(110, 45)

        change_button = QPushButton("変更")
        change_button.setStyleSheet("background-color: #F2C438; border-radius: 14px;")
        change_button.setFixedSize(140, 60)

        layout.addWidget(image_label, alignment=Qt.AlignLeft)
        layout.addWidget(work_time_label, alignment=Qt.AlignRight)
        layout.addWidget(work_time_combo, alignment=Qt.AlignRight)
        layout.addWidget(red_line)
        layout.addWidget(short_break_label, alignment=Qt.AlignRight)
        layout.addWidget(short_break_combo, alignment=Qt.AlignRight)
        layout.addWidget(blue_line)
        layout.addWidget(long_break_label, alignment=Qt.AlignRight)
        layout.addWidget(long_break_combo, alignment=Qt.AlignRight)
        layout.addWidget(blue_line)
        layout.addWidget(back_button, alignment=Qt.AlignRight)
        layout.addWidget(change_button, alignment=Qt.AlignRight)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication([])
    font = QFont('x12y12pxMaruMinya', 14)
    app.setFont(font)
    window = SettingsWindow()
    window.show()
    app.exec_()
