import pyglet.sprite


class Sprite(pyglet.sprite.Sprite):
    """
    Similar to the pyglet Sprite, but allow to change the width and height directly
    and update the size from a function
    """

    def __init__(self, *args, width: int = None, height: int = None, **kwargs):
        super().__init__(*args, **kwargs)

        self._orig_width: int = self.width
        self._orig_height: int = self.height

        if width is not None: self.width = width
        if height is not None: self.height = height

    # property

    @pyglet.sprite.Sprite.width.setter
    def width(self, width: int):
        self.scale_x = width / self._orig_width

    @pyglet.sprite.Sprite.height.setter
    def height(self, height: int):
        self.scale_y = height / self._orig_height

    # other event

    def update_size(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
