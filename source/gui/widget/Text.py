from typing import TYPE_CHECKING

from source.gui.widget import Widget

import pyglet

if TYPE_CHECKING:
    from source.gui.scene import Scene


class Text(Widget):
    """
    A widget that display a text
    """

    def __init__(self, scene: "Scene", *args, **kwargs):
        super().__init__(scene, *args, **kwargs)

        self.label = pyglet.text.Label(*args, **kwargs)

    def on_draw(self):
        self.label.draw()
