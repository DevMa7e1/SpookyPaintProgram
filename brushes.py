from scary_classes import Brush
from PIL import ImageDraw

class RoundBrush(Brush):
    def draw_point(self, image: ImageDraw.ImageDraw, color: tuple[int, int, int, int], size: int, current: tuple[int, int, float], last: tuple[int, int, float]):
        if abs(last[0] - current[0]) > abs(last[1] - current[1]):
            for x in range(last[0], current[0], 1 - 2 * int(current[0] < last[0])):
                y = last[1] + (x - last[0]) / (current[0] - last[0]) * (current[1] - last[1])
                s = (last[2] + (x - last[0]) / (current[0] - last[0]) * (current[2] - last[2])) * size
                image.circle((x, y), s/2, fill=color)
        else:
            for y in range(last[1], current[1], 1 - 2 * int(current[1] < last[1])):
                x = last[0] + (y - last[1]) / (current[1] - last[1]) * (current[0] - last[0])
                s = (last[2] + (y - last[1]) / (current[1] - last[1]) * (current[2] - last[2])) * size
                image.circle((x, y), s/2, fill=color)

class VerticalLineBrush(Brush):
    def draw_point(self, image: ImageDraw.ImageDraw, color: tuple[int, int, int, int], size: int, current: tuple[int, int, float], last: tuple[int, int, float]):
        topleft = (last[0], last[1])
        topright = (last[0] + int(last[2]*size), last[1])
        bottomleft = (current[0], current[1])
        bottomright = (current[0] + int(current[2]*size), current[1])
        image.polygon((topleft, topright, bottomright, bottomleft), fill = color)

class HorizontalLineBrush(Brush):
    def draw_point(self, image: ImageDraw.ImageDraw, color: tuple[int, int, int, int], size: int, current: tuple[int, int, float], last: tuple[int, int, float]):
        topleft = (last[0], last[1])
        topright = (last[0], last[1] + int(last[2]*size))
        bottomleft = (current[0], current[1])
        bottomright = (current[0], current[1] + int(current[2]*size))
        image.polygon((topleft, topright, bottomright, bottomleft), fill = color)

available_brushes: list[type] = [VerticalLineBrush, HorizontalLineBrush, RoundBrush]