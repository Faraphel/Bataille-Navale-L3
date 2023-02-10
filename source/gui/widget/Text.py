from typing import TYPE_CHECKING

from source.gui.widget.abc import BoxWidget

import pyglet

from source.type import Percentage

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Text(BoxWidget):
    """
    A widget that display a text
    """

    def __init__(self, scene: "Scene",
                 x: Percentage = 0,
                 y: Percentage = 0,
                 width: Percentage = None,
                 height: Percentage = None,
                 *args, **kwargs):
        super().__init__(scene, x, y, width, height)

        self.label = pyglet.text.Label(
            x=self.x, y=self.y, width=self.width, height=self.height,
            *args, **kwargs
        )

    def on_resize(self, width: int, height: int):
        self.label.x = self.x
        self.label.y = self.y
        self.label.width = self.width
        self.label.height = self.height

    def on_draw(self):
        self.label.draw()
