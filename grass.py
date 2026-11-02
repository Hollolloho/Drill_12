from pathlib import Path

from pico2d import load_image

class Grass:
    def __init__(self):
        self.image = load_image(str(Path(__file__).with_name('grass.png')))
        self.x, self.y = 400, 30
    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass
