from scary_classes import Brush
from PIL import ImageDraw
import math

class VerticalLineBrush(Brush):
    def draw_point(self, image: ImageDraw.ImageDraw, color: tuple[int, int, int, int], current: tuple[int, int, float], last: tuple[int, int, float]):
        topleft = (last[0], last[1])
        topright = (last[0] + int(last[2]*20), last[1])
        bottomleft = (current[0], current[1])
        bottomright = (current[0] + int(current[2]*20), current[1])
        image.polygon((topleft, topright, bottomright, bottomleft), fill = color)

class HorizontalLineBrush(Brush):
    def draw_point(self, image: ImageDraw.ImageDraw, color: tuple[int, int, int, int], current: tuple[int, int, float], last: tuple[int, int, float]):
        topleft = (last[0], last[1])
        topright = (last[0], last[1] + int(last[2]*20))
        bottomleft = (current[0], current[1])
        bottomright = (current[0], current[1] + int(current[2]*20))
        image.polygon((topleft, topright, bottomright, bottomleft), fill = color)

class RotatingLineBrush(Brush):
    @staticmethod
    def rotate_point(x: int, y: int, angle: float):
        angle = angle / 180 * math.pi
        nx = x * math.cos(angle) - y * math.sin(angle)
        ny = y * math.cos(angle) + x * math.sin(angle)
        return nx, ny
    
    def draw_point(self, image: ImageDraw.ImageDraw, color: tuple[int, int, int, int], current: tuple[int, int, float], last: tuple[int, int, float]):
        rotation = abs(math.atan2(current[1]-last[1], current[0]-last[0]))
        factor = self.rotate_point(0, int(20*last[2]), rotation/2)
        
        topleft = (last[0], last[1])
        topright = (last[0] + factor[0], last[1] + factor[1])
        bottomleft = (current[0], current[1])
        bottomright = (current[0] + factor[0], current[1] + factor[1])
        image.polygon((topleft, topright, bottomright, bottomleft), fill = color)

available_brushes: list[type] = [RotatingLineBrush, VerticalLineBrush, HorizontalLineBrush]