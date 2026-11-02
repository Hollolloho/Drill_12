from pathlib import Path

from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    image = None

    def __init__(self, x, y, direction):
        self.x, self.y = x, y
        self.direction = direction
        if Ball.image is None:
            Ball.image = load_image(str(Path(__file__).with_name('ball21x21.png')))

    def update(self):
        self.x += self.direction * 10
        if self.x < -21 or self.x > get_canvas_width() + 21:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
