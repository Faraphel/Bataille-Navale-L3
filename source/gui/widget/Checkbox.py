from typing import TYPE_CHECKING

import pyglet.image

from source.gui.sprite import Sprite
from source.gui.widget.abc import BoxWidget
from source.type import Distance


if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Checkbox(BoxWidget):
    def __init__(self, scene: "Scene",

                 texture_disabled: pyglet.image.AbstractImage,
                 texture_enabled: pyglet.image.AbstractImage,

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,

                 state: bool = False,

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self._texture_disabled = texture_disabled
        self._texture_enabled = texture_enabled

        self.tick = Sprite(img=self._texture_disabled, **kwargs)

        self.state = state

        self._refresh_size()

    # refreshing

    @property
    def tick_texture(self):
        return self._texture_enabled if self.state else self._texture_disabled

    def _refresh_tick(self):
        self.tick.image = self.tick_texture

    def _refresh_size(self):
        self.tick.x, self.tick.y = self.x, self.y
        self.tick.width, self.tick.height = self.width, self.height

    # property

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: bool):
        self._state = state
        self._refresh_tick()

    # event

    def on_resize(self, width: int, height: int):
        self._refresh_size()

    def on_release(self, button: int, modifiers: int):
        # lorsque le bouton est enclenché, inverse son état
        self.state = not self.state

    def draw(self):
        self.tick.draw()
