from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
import sys
from scary_classes import *
from pathlib import Path
from scary_drawing_window import PaintWindow

class WelcomeScreen(QMainWindow):
    def __init__(self, /, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        mainbox = QVBoxLayout()
        self.setStyleSheet('background-color: black;')

        hfont = QFont(QFontDatabase.applicationFontFamilies( \
        QFontDatabase.addApplicationFont(str(Path(__file__).parent.absolute().joinpath(f'assets/Underdog-Regular.ttf'))))[0])
        hfont.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        hfont.setStyleStrategy(QFont.StyleStrategy.NoAntialias)

        welcome_text = QLabel(self)
        welcome_text.setText('Spooky Paint Program')
        hfont.setPixelSize(42)
        welcome_text.setFont(hfont)
        welcome_text.setStyleSheet('color: purple;')
        mainbox.addWidget(welcome_text)

        new_drawing_container = QWidget()
        new_drawing_box = QHBoxLayout()
        new_drawing_container.setLayout(new_drawing_box)
        new_drawing_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        new_drawing = QPushButton(self)
        new_drawing.setText('Create a new drawing')
        new_drawing.pressed.connect(self.proceed)
        new_drawing.setStyleSheet('border-radius: 0px; background-color: orange; padding: 4px;')
        hfont.setPixelSize(16)
        new_drawing.setFont(hfont)
        new_drawing_box.addWidget(new_drawing)
        mainbox.addWidget(new_drawing_container)

        main = QWidget()
        main.setLayout(mainbox)
        self.setCentralWidget(main)
    def proceed(self):
        paintwindow = PaintWindow()
        paintwindow.show()
        self.close()


app = QApplication(sys.argv)

window = WelcomeScreen()
window.show()

app.exec()