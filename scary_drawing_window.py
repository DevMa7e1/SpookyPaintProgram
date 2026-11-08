from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent, QTabletEvent, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog, QColorDialog, \
QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QSpinBox
from PIL import Image, ImageDraw
import numpy as np
from scary_classes import *
import brushes
from copy import copy

def toQPixmap(img: Image.Image):
    return QPixmap.fromImage(img.toqimage())

class DrawArea(QLabel):
    def __init__(self, parent: PaintWindow) -> None:
        super().__init__('', parent)
        self.draw_space = (700, 500)
        self.setFixedSize(*self.draw_space)
        self.mw = parent
        self.setStyleSheet('background-color: white;')

        self.image = Image.fromarray(np.zeros((self.draw_space[1], self.draw_space[0], 4), np.uint8), mode='RGBA')
        self.preview = self.image.copy()
        self.previewdraw = ImageDraw.ImageDraw(self.preview)
        self.setPixmap(toQPixmap(self.image))
        self.stroke = Stroke()
        self.strokes = []
        self.undoed = []

    def process_stroke(self):
        draw = ImageDraw.ImageDraw(self.image)
        self.strokes.append((copy(self.stroke.encoded), copy(self.mw.current_color), copy(self.mw.current_brush), copy(self.mw.current_size)))
        if not self.stroke.empty():
            points = self.stroke.decode()
            last = next(points)
            if next(points, (-1, -1, -1)) != (-1, -1, -1):
                self.undoed.clear()
                for point in self.stroke.decode():
                    self.mw.current_brush.draw_point(draw, self.mw.current_color, self.mw.current_size, (point[0], point[1], point[2]/65535), (last[0], last[1], last[2]/65535))
                    last = point
            self.setPixmap(toQPixmap(self.image))

    def end_stroke(self):
        self.strokes.append((copy(self.stroke.encoded), copy(self.mw.current_color), copy(self.mw.current_brush), copy(self.mw.current_size)))
        self.stroke.clear()
        self.undoed.clear()

    def process_in_real_time(self, x: int, y: int, pressure: float):
        draw = ImageDraw.ImageDraw(self.image)
        if not self.stroke.empty():
            self.mw.current_brush.draw_point(draw, self.mw.current_color, self.mw.current_size, (x, y, pressure), self.stroke.get_last())
            self.stroke.add(x, y, pressure)
            self.setPixmap(toQPixmap(self.image))
        else:
            self.stroke.add(x, y, pressure)
    
    def mouseReleaseEvent(self, a0: QMouseEvent | None) -> None:
        self.end_stroke()
        if type(a0) == QMouseEvent:
            return a0.accept()
        else: 
            return None
    
    def tabletEvent(self, a0: QTabletEvent | None) -> None:
        if type(a0) == QTabletEvent:
            if a0.buttons() == Qt.MouseButton.LeftButton:
                if a0.position().x() > 0 and a0.position().x() < self.draw_space[0] and a0.position().y() > 0 and a0.position().y() < self.draw_space[1]:
                    self.process_in_real_time(int(a0.position().x()), int(a0.position().y()), a0.pressure())
                return a0.accept()
            else:
                self.end_stroke()
                return a0.accept()
        return super().tabletEvent(a0)
    
    def mouseMoveEvent(self, ev: QMouseEvent | None) -> None:
        if type(ev) == QMouseEvent:
            if ev.buttons() == Qt.MouseButton.LeftButton:
                if ev.position().x() > 0 and ev.position().x() < self.draw_space[0] and ev.position().y() > 0 and ev.position().y() < self.draw_space[1]:
                    self.process_in_real_time(int(ev.position().x()), int(ev.position().y()), 1)
        return super().mouseMoveEvent(ev)

    def undo(self):
        if len(self.strokes) > 0:
            self.undoed.append(self.strokes.pop())
            self.image = Image.fromarray(np.zeros((self.draw_space[1], self.draw_space[0], 4), np.uint8), mode='RGBA')
            for i in self.strokes:
                redo = Stroke()
                redo.encoded = i[0]

                draw = ImageDraw.ImageDraw(self.image)
                if not redo.empty():
                    points = redo.decode()
                    last = next(points)
                    if next(points, (-1, -1, -1)) != (-1, -1, -1):
                        for point in redo.decode():
                            i[2].draw_point(draw, i[1], i[3], (point[0], point[1], point[2]/65535), (last[0], last[1], last[2]/65535))
                            last = point
            self.setPixmap(toQPixmap(self.image))
            self.preview = self.image.copy()
            self.previewdraw = ImageDraw.ImageDraw(self.preview)

    def redo(self):
        if len(self.undoed) > 0:
            self.strokes.append(self.undoed.pop())
            i = self.strokes[-1]
            redo = Stroke()
            redo.encoded = i[0]

            draw = ImageDraw.ImageDraw(self.image)
            if not redo.empty():
                points = redo.decode()
                last = next(points)
                if next(points, (-1, -1, -1)) != (-1, -1, -1):
                    first = True
                    for point in redo.decode():
                        i[2].draw_point(draw, i[1], i[3], (point[0], point[1], point[2]/65535), (last[0], last[1], last[2]/65535))
                        last = point
                        first = False
            self.setPixmap(toQPixmap(self.image))
            self.preview = self.image.copy()
            self.previewdraw = ImageDraw.ImageDraw(self.preview)

class PaintWindow(QWidget):
    def __init__(self, /, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Spooky Paint Program')

        self.setStyleSheet('background-color: #AAAAAA')
        self.mainbox = QVBoxLayout()
        self.mainbox.setContentsMargins(0, 0, 0, 0)

        self.central = DrawArea(self)
        self.mainbox.addWidget(self.central)

        self.current_brush = brushes.VerticalLineBrush()
        self.current_color = (0, 0, 0, 255)
        self.current_size = 20

        menuwidget = QWidget()
        menuwidget.setStyleSheet('background-color: #FFC568')
        menubar = QHBoxLayout()
        menubar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        menuwidget.setLayout(menubar)

        undo_action = QPushButton(self)
        undo_action.setStyleSheet('background-color: #FF7518;')
        undo_action.setText('Undo')
        undo_action.setToolTip('Undo the previous stroke')
        undo_action.pressed.connect(self.central.undo)
        menubar.addWidget(undo_action)

        redo_action = QPushButton(self)
        redo_action.setStyleSheet('background-color: #FF7518;')
        redo_action.setText('Redo')
        redo_action.setToolTip('Redoes the previously undone stroke')
        redo_action.pressed.connect(self.central.redo)
        menubar.addWidget(redo_action)

        save_action = QPushButton(self)
        save_action.setStyleSheet('background-color: #FF7518;')
        save_action.setText('Save')
        save_action.setToolTip('Save the current drawing to a picture file')
        save_action.pressed.connect(self.save)
        menubar.addWidget(save_action)

        color_action = QPushButton(self)
        color_action.setStyleSheet('background-color: #FF7518;')
        color_action.setText('Set color')
        color_action.setToolTip('Set the color of the brush')
        color_action.pressed.connect(self.select_color)
        menubar.addWidget(color_action)

        size_container = QWidget()
        size_box = QHBoxLayout()
        pixel_size = QSpinBox()
        pixel_size.setMaximum(500)
        pixel_size.setValue(20)
        pixel_size.valueChanged.connect(self.change_size)
        self.psize = pixel_size
        pixel_label = QLabel()
        pixel_label.setText('Brush size (px): ')
        size_box.addWidget(pixel_label)
        size_box.addWidget(pixel_size)
        size_container.setLayout(size_box)
        menubar.addWidget(size_container)

        self.brush_select = QComboBox()
        self.brush_select.setStyleSheet('background-color: #FF7518;')
        for i in brushes.available_brushes:
            self.brush_select.addItem(i.__name__, userData=i)
        self.brush_select.currentIndexChanged.connect(self.change_brush)
        menubar.addWidget(self.brush_select)

        self.mainbox.addWidget(menuwidget)
        self.setLayout(self.mainbox)

    def change_size(self):
        self.current_size = self.psize.value()

    def change_brush(self):
        self.current_brush = self.brush_select.itemData(self.brush_select.currentIndex())()
    
    def save(self):
        self.filediag = QFileDialog(self, 'Save drawing', filter='PNG Image (*.png)')
        self.filediag.setFileMode(QFileDialog.FileMode.AnyFile)
        self.filediag.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        self.filediag.accepted.connect(self.save_file)
        self.filediag.show()
    def save_file(self):
        if self.filediag.selectedNameFilter() == 'PNG Image (*.png)':
            if not self.filediag.selectedFiles()[0].endswith('.png'):
                self.central.image.save(self.filediag.selectedFiles()[0]+'.png')
            else:
                self.central.image.save(self.filediag.selectedFiles()[0])

    def select_color(self):
        self.cdiag = QColorDialog(self)
        color = self.cdiag.getColor()
        if color.isValid():
            self.current_color = (color.toRgb().red(), color.toRgb().green(), color.toRgb().blue(), 255)