import pyglet

from source.gui.better_pyglet.abc import Element


class Sprite(Element, pyglet.sprite.Sprite):
    """
    Same as the pyglet sprite, but allow to set a width and height easier
    """

    def __init__(self, width: int = None, height: int = None, *args, **kwargs):
        super().__init__(*args, **(self.default_kwargs | kwargs))

        self._orig_width: int = self.width
        self._orig_height: int = self.height

        if width is not None: self.width = width
        if height is not None: self.height = height

    @pyglet.sprite.Sprite.width.setter
    def width(self, width: int):
        self.scale_x = width / self._orig_width

    @pyglet.sprite.Sprite.height.setter
    def height(self, height: int):
        self.scale_y = height / self._orig_height
