from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont, QFontDatabase, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
import sys
from scary_classes import *
from pathlib import Path
from scary_drawing_window import PaintWindow

class WelcomeScreen(QMainWindow):
    def __init__(self, /, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle('Spooky Paint Program')
        self.setWindowIcon(QIcon(str(Path(__file__).parent.absolute().joinpath(f'assets/pumpkin.png'))))
        mainbox = QVBoxLayout()
        mainbox.setAlignment(Qt.AlignmentFlag.AlignTop)

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
        self.newd = new_drawing
        new_drawing.setStyleSheet('border-radius: 0px; background-color: orange; padding: 4px;')
        hfont.setPixelSize(18)
        new_drawing.setFont(hfont)
        new_drawing_box.addWidget(new_drawing)
        new_drawing_container.setStyleSheet('padding: 0px; margin: 0px;')
        mainbox.addWidget(new_drawing_container, Qt.AlignmentFlag.AlignTop)

        pumpkin_deco = QLabel()
        pumpkin_deco.setStyleSheet('')
        path = str(Path(__file__).parent.absolute().joinpath(f'assets/pumpkin.png'))
        pumpkin_deco.setPixmap(QPixmap(path).scaled(120, 110))
        mainbox.addWidget(pumpkin_deco, alignment=Qt.AlignmentFlag.AlignRight)

        path = str(Path(__file__).parent.absolute().joinpath(f'assets/welcome-bg.png').as_posix())
        main = QWidget()
        main.setLayout(mainbox)
        main.setObjectName('bgd')
        self.setCentralWidget(main)
        main.setStyleSheet(f'#bgd {{border-image: url({path}) 0 0 0 0 stretch stretch;}}')
        main.setFixedSize(QSize(450, 300))

    def proceed(self):
        self.newd.pressed.disconnect()
        paintwindow = PaintWindow()
        paintwindow.show()
        self.close()


app = QApplication(sys.argv)

window = WelcomeScreen()
window.show()

app.exec()