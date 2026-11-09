from PIL import ImageDraw

class Brush:
    name = 'Default brush name'
    def draw_point(self, image: ImageDraw.ImageDraw, color: tuple[int, int, int, int], size: int, current: tuple[int, int, float], last: tuple[int, int, float]):
        pass

class Stroke:
    def __init__(self) -> None:
        self.points: list[tuple[int, int, int]] = []
        self.encoded = bytes()
    def add(self, x: int, y: int, pressure: float):
        self.encoded += x.to_bytes(2, 'big')
        self.encoded += y.to_bytes(2, 'big')
        self.encoded += int(pressure * 65535).to_bytes(2, 'big')
    def decode(self):
        for i in range(0, len(self.encoded), 6):
            yield (int.from_bytes(self.encoded[i:i+2], 'big'), int.from_bytes(self.encoded[i+2:i+4], 'big'), int.from_bytes(self.encoded[i+4:i+6], 'big'))
        return
    def empty(self):
        if len(self.encoded) > 0:
            return False
        return True
    def get_last(self):
        return (int.from_bytes(self.encoded[len(self.encoded)-6:len(self.encoded)-4], 'big'), int.from_bytes(self.encoded[len(self.encoded)-4:len(self.encoded)-2], 'big'), int.from_bytes(self.encoded[len(self.encoded)-2:], 'big')/65535)
    def clear(self):
        self.encoded = bytes()