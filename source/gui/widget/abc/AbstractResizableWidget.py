from abc import ABC
from typing import Optional, TYPE_CHECKING

from source.gui.widget.abc import AbstractBoxWidget
from source.type import Percentage


if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.scene.abc import AbstractScene


class AbstractResizableWidget(AbstractBoxWidget, ABC):
    def __init__(self, x: int | Percentage, y: int | Percentage, width: int | Percentage, height: int | Percentage):
        super().__init__(x, y, width, height)

        self._window_width: Optional[int] = None
        self._window_height: Optional[int] = None

    # getter / setter

    def on_window_added(self, window: "Window", scene: "AbstractScene"):
        self._window_width = window.width
        self._window_height = window.height

    @property
    def x(self) -> int:
        return self._x * self._window_width if isinstance(self._x, Percentage) else self._x

    @property
    def y(self) -> int:
        return self._y * self._window_height if isinstance(self._y, Percentage) else self._y

    @property
    def width(self) -> int:
        return self._width * self._window_width if isinstance(self._width, Percentage) else self._width

    @property
    def height(self) -> int:
        return self._height * self._window_height if isinstance(self._height, Percentage) else self._height

    # event

    def update_size(self): pass

    def on_resize(self, window: "Window", scene: "AbstractScene", width: int, height: int):
        self._window_width = width
        self._window_height = height

        self.update_size()
