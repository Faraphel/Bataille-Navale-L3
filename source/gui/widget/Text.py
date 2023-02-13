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
            *args, **kwargs
        )

        self._refresh_size()

    def _refresh_size(self):
        self.label.x = self.x
        self.label.y = self.y
        self.label.width = self.width
        self.label.height = self.height

    def on_resize(self, width: int, height: int):
        self._refresh_size()

    def draw(self):
        """
        The draw function. Can be called to draw the widget, but can be ignored to draw it with batchs.
        """

        self.label.draw()
