from typing import Optional

from source.gui.widget.base import BaseBoxWidget
from source.type import Percentage


class BaseAdaptativeWidget(BaseBoxWidget):
    def __init__(self, x: int | Percentage, y: int | Percentage, width: int | Percentage, height: int | Percentage):
        super().__init__(x, y, width, height)

        self._window_width: Optional[int] = None
        self._window_height: Optional[int] = None

    # getter / setter

    def on_window_added(self, window: "Window", scene: "BaseScene"):
        self._window_width = window.width
        self._window_height = window.height

    @property
    def x(self) -> int:
        return self._x if isinstance(self._x, int) else self._x * self._window_width

    @property
    def y(self) -> int:
        return self._y if isinstance(self._y, int) else self._y * self._window_height

    @property
    def width(self) -> int:
        return self._width if isinstance(self._width, int) else self._width * self._window_width

    @property
    def height(self) -> int:
        return self._height if isinstance(self._height, int) else self._height * self._window_height

    # event

    def update_size(self): pass

    def on_resize(self, window: "Window", scene: "BaseScene", width: int, height: int):
        self._window_width = width
        self._window_height = height

        self.update_size()
