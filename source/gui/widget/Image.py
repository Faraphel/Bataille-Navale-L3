from typing import TYPE_CHECKING

import pyglet.image

from source.gui.sprite import Sprite
from source.gui.widget.abc import BoxWidget
from source.type import Percentage


if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Image(BoxWidget):
    def __init__(self, scene: "Scene",

                 image: pyglet.image.AbstractImage,

                 x: Percentage = 0,
                 y: Percentage = 0,
                 width: Percentage = None,
                 height: Percentage = None,
                 *args, **kwargs):
        super().__init__(scene, x, y, width, height)

        self.image = Sprite(img=image, *args, **kwargs)

        self._refresh_size()

    # refresh

    def _refresh_size(self):
        self.image.width, self.image.height = self.width, self.height

    # event

    def on_resize(self, width: int, height: int):
        self._refresh_size()

    # draw

    def draw(self):
        self.image.draw()