from typing import TYPE_CHECKING, Type

from source.gui.sprite import Sprite
from source.gui.texture.abc import Style
from source.gui.widget.abc import BoxWidget
from source.type import Distance


if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Checkbox(BoxWidget):
    """
    A checkbox widget with a background texture that change depending on if it is checked or unchecked.
    """

    def __init__(self, scene: "Scene",

                 style: Type[Style],

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,

                 state: bool = False,

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self.style = style

        self.tick = Sprite(img=self.style.disabled, **kwargs)

        self.state = state

        self.add_listener("on_click_release", lambda *_: self.swap_state())

        self._refresh_size()

    # refreshing

    @property
    def tick_texture(self):
        return self.style.get("enabled" if self.state else "disabled")

    def _refresh_tick(self):
        self.tick.image = self.tick_texture

    def _refresh_size(self):
        self.tick.x, self.tick.y = self.xy
        self.tick.width, self.tick.height = self.size

    # property

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: bool):
        self._state = state
        self.trigger_event("on_state_change")
        self.trigger_event("on_checked" if state else "on_unchecked")
        self._refresh_tick()

    def swap_state(self):
        self.state = not self.state  # inverse l'état

    # event

    def on_resize(self, width: int, height: int):
        self._refresh_size()

    def draw(self):
        self.tick.draw()
