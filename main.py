from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent, QTabletEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
QFileDialog, QColorDialog, QPushButton, QWidget, QHBoxLayout, QVBoxLayout
from PIL import Image, ImageDraw
import numpy as np
import sys
from scary_classes import *
import brushes
from time import time

app = QApplication(sys.argv)

def toQPixmap(img: Image.Image):
    return QPixmap.fromImage(img.toqimage())

class MainWindow(QMainWindow):
    def __init__(self, /, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Spooky Paint Program')

        self.mainbox = QVBoxLayout()

        self.central = QLabel()
        self.mainbox.addWidget(self.central)

        self.draw_space = (700, 500)
        self.central.setFixedSize(*self.draw_space)

        self.image = Image.fromarray(np.zeros((self.draw_space[1], self.draw_space[0], 4), np.uint8), mode='RGBA')
        self.preview = self.image.copy()
        self.previewdraw = ImageDraw.ImageDraw(self.preview)
        self.central.setPixmap(toQPixmap(self.image))

        self.stroke = Stroke()
        self.current_brush = brushes.VerticalLineBrush()
        self.current_color = (0, 0, 0, 255)

        menuwidget = QWidget()
        menubar = QHBoxLayout()
        menuwidget.setLayout(menubar)

        save_action = QPushButton(self)
        save_action.setText('Save')
        save_action.setToolTip('Save the current drawing to a picture file')
        save_action.pressed.connect(self.save)
        menubar.addWidget(save_action)

        color_action = QPushButton(self)
        color_action.setText('Set color')
        color_action.setToolTip('Set the color of the brush')
        color_action.pressed.connect(self.select_color)
        menubar.addWidget(color_action)

        self.mainbox.addWidget(menuwidget)

        main = QWidget()
        main.setLayout(self.mainbox)
        self.setCentralWidget(main)
    
    def tabletEvent(self, a0: QTabletEvent | None) -> None:
        if type(a0) == QTabletEvent:
            if a0.position().x() > 0 and a0.position().x() < self.draw_space[0] and a0.position().y() > 0 and a0.position().y() < self.draw_space[1]:
                self.stroke.add(int(a0.position().x()), int(a0.position().y()), a0.pressure())
                self.previewdraw.line(((int(a0.position().x()), int(a0.position().y())), (int(a0.position().x()) + a0.pressure()*20, int(a0.position().y()))), fill=(100, 100, 100, 255))
                self.central.setPixmap(toQPixmap(self.preview))
            else:
                self.process_stroke()
        return super().tabletEvent(a0)
    def save(self):
        self.filediag = QFileDialog(self, 'Save drawing', filter='PNG Image (*.png)')
        self.filediag.setFileMode(QFileDialog.FileMode.AnyFile)
        self.filediag.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        self.filediag.accepted.connect(self.save_file)
        self.filediag.show()
    def save_file(self):
        self.image.save(self.filediag.selectedFiles()[0])

    def select_color(self):
        self.cdiag = QColorDialog(self)
        color = self.cdiag.getColor()
        if color.isValid():
            self.current_color = (color.toRgb().red(), color.toRgb().green(), color.toRgb().blue(), 255)
    
    def process_stroke(self):
        draw = ImageDraw.ImageDraw(self.image)
        if not self.stroke.empty():
            points = self.stroke.decode()
            last = next(points)
            if next(points, (-1, -1, -1)) != (-1, -1, -1):
                for point in self.stroke.decode():
                    self.current_brush.draw_point(draw, self.current_color, (point[0], point[1], point[2]/65535), (last[0], last[1], last[2]/65535))
                    last = point
            self.central.setPixmap(toQPixmap(self.image))
        self.stroke.clear()
        self.preview = self.image.copy()
        self.previewdraw = ImageDraw.ImageDraw(self.preview)
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        self.process_stroke()
        return super().mouseReleaseEvent(a0)

window = MainWindow()
window.show()

app.exec()