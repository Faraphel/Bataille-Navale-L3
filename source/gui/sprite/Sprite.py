import pyglet.sprite


class Sprite(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._orig_width: int = self.width
        self._orig_height: int = self.height

    @pyglet.sprite.Sprite.width.setter
    def width(self, width: int):
        self.scale_x = width / self._orig_width

    @pyglet.sprite.Sprite.height.setter
    def height(self, height: int):
        self.scale_y = height / self._orig_height
