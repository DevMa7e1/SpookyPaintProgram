from scary_classes import Brush
from PIL import ImageDraw

class VerticalLineBrush(Brush):
    def draw_point(self, image: ImageDraw.ImageDraw, current: tuple[int, int, float], last: tuple[int, int, float]):
        topleft = (last[0], last[1])
        topright = (last[0] + int(last[2]*20), last[1])
        bottomleft = (current[0], current[1])
        bottomright = (current[0] + int(current[2]*20), current[1])
        image.polygon((topleft, topright, bottomright, bottomleft), fill = (0, 0, 0, 255))

class HorizontalLineBrush(Brush):
    def draw_point(self, image: ImageDraw.ImageDraw, current: tuple[int, int, float], last: tuple[int, int, float]):
        topleft = (last[0], last[1])
        topright = (last[0], last[1] + int(last[2]*20))
        bottomleft = (current[0], current[1])
        bottomright = (current[0], current[1] + int(current[2]*20))
        image.polygon((topleft, topright, bottomright, bottomleft), fill = (0, 0, 0, 255))