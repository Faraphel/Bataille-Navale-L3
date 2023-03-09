from typing import TYPE_CHECKING, Callable, Any, Type

from source.gui.better_pyglet import Sprite, Label
from source.gui.texture.abc import Style
from source.gui.widget.abc import BoxWidget
from source.type import Distance
from source.utils import dict_filter_prefix, in_bbox

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Scroller(BoxWidget):
    """
    A scroller widget with a background texture, a scroller and a label.
    The cursor can be moved between the "from" and the "to" value
    """

    def __init__(self, scene: "Scene",

                 style: Type[Style],

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

        self.style = style

        self.cursor_width = cursor_width
        self.text_transform = text_transform

        self.background = Sprite(
            img=self.style.get("background"),
            batch=self.scene.batch,
            **dict_filter_prefix("background_", kwargs)
        )

        self.cursor = Sprite(
            img=self.style.get("cursor"),
            batch=self.scene.batch,
            **dict_filter_prefix("cursor_", kwargs)
        )

        self.label = Label(
            anchor_x="center", anchor_y="center",
            batch=self.scene.batch,
            **dict_filter_prefix("label_", kwargs)
        )

        self.add_listener("on_click_release", lambda _, rel_x, *__: self._refresh_cursor(rel_x))

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
        self.value = (rel_x / self.width) * (self.to - self.from_) + self.from_

    # property

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        if not self.from_ <= value <= self.to: raise ValueError(f"The value is not in range")
        self._value = value
        self.trigger_event("on_value_change")
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

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if in_bbox((x, y), self.bbox):
            self._refresh_cursor(x - self.x)
