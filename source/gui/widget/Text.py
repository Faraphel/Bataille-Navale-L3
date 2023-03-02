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

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self.label = pyglet.text.Label(
            x=self.x, y=self.y, width=self.width, height=self.height,
            batch=self.scene.batch,
            **kwargs
        )

        self._refresh_size()

    @property
    def text(self):
        return self.label.text

    @text.setter
    def text(self, text: str):
        self.label.text = text

    def _refresh_size(self):
        self.label.x, self.label.y = self.xy
        self.label.width, self.label.height = self.size

    def on_resize(self, width: int, height: int):
        self._refresh_size()
