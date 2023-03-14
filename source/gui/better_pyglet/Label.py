import pyglet

from source.gui.better_pyglet.abc import Element


class Label(Element, pyglet.text.Label):
    """
    Un label de base de pyglet, mais supportant les arguments par défaut
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **(self.default_kwargs | kwargs))
