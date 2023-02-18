from typing import TYPE_CHECKING, Callable, Any

import pyglet.image

from source.gui.sprite import Sprite
from source.gui.widget.abc import BoxWidget
from source.type import Distance
from source.utils import dict_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Scroller(BoxWidget):
    def __init__(self, scene: "Scene",

                 texture_background: pyglet.image.AbstractImage,
                 texture_cursor: pyglet.image.AbstractImage,

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,

                 from_: float = 0,
                 value: float = 0.5,
                 to: float = 1,

                 cursor_width: Distance = 0.1,
                 text_transform: Callable[[float], Any] = lambda value: value,

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self.cursor_width = cursor_width
        self.text_transform = text_transform

        self.background = Sprite(
            img=texture_background,
            **dict_prefix("background_", kwargs)
        )
        self.cursor = Sprite(
            img=texture_cursor,
            **dict_prefix("cursor_", kwargs)
        )
        self.label = pyglet.text.Label(
            anchor_x="center", anchor_y="center",
            **dict_prefix("label_", kwargs)
        )

        self.add_listener("on_click_release", lambda rel_x, *_: self._refresh_cursor(rel_x))

        self._from = from_
        self._to = to
        self.value = value

    # refresh

    def _refresh(self):
        # background
        self.background.x, self.background.y = self.xy
        self.background.width, self.background.height = self.size

        # cursor
        self.cursor.width = self.width * self.cursor_width
        self.cursor.height = self.height
        self.cursor.y = self.y
        self.cursor.x = (
                # the base offset
                self.x
                # position the cursor relatively to the start and the end of the range
                + (self.value - self.from_) / (self.to - self.from_) * self.background.width
                # center the cursor with its own width
                - (self.cursor.width / 2)
        )

        # label
        self.label.x, self.label.y = self.center
        self.label.text = str(self.text_transform(self.value))

    def _refresh_cursor(self, rel_x: int):
        self.value = rel_x / self.width

    # property

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        if not self.from_ <= value <= self.to: raise ValueError(f"The value is not in range")
        self._value = value
        self._refresh()

    @property
    def from_(self):
        return self._from

    @from_.setter
    def from_(self, from_: float):
        self._from = from_
        self._refresh()

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, to: float):
        self._to = to
        self._refresh()

    # event

    def on_resize(self, width: int, height: int):
        self._refresh()

    def draw(self):
        self.background.draw()
        self.cursor.draw()
        self.label.draw()
