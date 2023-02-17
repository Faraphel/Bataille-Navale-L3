from typing import TYPE_CHECKING

import pyglet.image

from source.gui.sprite import Sprite
from source.gui.widget.abc import BoxWidget
from source.type import Distance

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Image(BoxWidget):
    def __init__(self, scene: "Scene",

                 image: pyglet.image.AbstractImage,

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self.image = Sprite(img=image, **kwargs)

        self._refresh_size()

    # refresh

    def _refresh_size(self):
        self.image.width, self.image.height = self.size

    # event

    def on_resize(self, width: int, height: int):
        self._refresh_size()

    # draw

    def draw(self):
        self.image.draw()
