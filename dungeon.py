from pico2d import load_image


class Dungeon:
    def __init__(self, x = 960, y = 900):
        self.image = load_image('image\\Background.png')
        self.x, self.y = x, y

    def draw(self):
        self.image.draw(self.x / 2, self.y / 2)

    def update(self):
        pass