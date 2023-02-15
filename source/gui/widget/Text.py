from typing import TYPE_CHECKING

from source.gui.widget.abc import BoxWidget

import pyglet

from source.type import Distance

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Text(BoxWidget):
    """
    A widget that display a text
    """

    def __init__(self, scene: "Scene",
                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,
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
        self.label.draw()
