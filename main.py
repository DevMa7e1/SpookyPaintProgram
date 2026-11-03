from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTabletEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PIL import Image
import numpy as np
import sys

app = QApplication(sys.argv)

def toQPixmap(img: Image.Image):
    return QPixmap.fromImage(img.toqimage())

class MainWindow(QMainWindow):
    def __init__(self, /, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Main Window')
        self.central = QLabel()
        self.central.setFixedSize(700, 500)
        self.image = Image.fromarray(np.zeros((500, 700, 4), np.uint8), mode='RGBA')
        self.central.setPixmap(toQPixmap(self.image))
        self.setCentralWidget(self.central)
    def tabletEvent(self, a0: QTabletEvent | None) -> None:
        if type(a0) == QTabletEvent:
            for i in range(int(a0.pressure()*20)):
                self.image.putpixel((int(a0.position().x()) + i, int(a0.position().y())), (0, 0, 0, 255))
                self.central.setPixmap(toQPixmap(self.image))
        return super().tabletEvent(a0)

window = MainWindow()
window.show()

app.exec()