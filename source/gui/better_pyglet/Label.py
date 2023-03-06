import pyglet

from source.gui.better_pyglet.abc import Element


class Label(Element, pyglet.text.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **(self.default_kwargs | kwargs))
