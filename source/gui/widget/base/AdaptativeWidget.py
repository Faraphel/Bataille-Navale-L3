from source.gui.widget.base import Widget

from typing import TYPE_CHECKING

from source.type import BBox, Percentage

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.scene.base import Scene


class AdaptativeWidget(Widget):
    """
    Similar to a normal Widget

    If the x, y, width or height is a float (representing a percentage), it will change depending on the window size
    """

    def __init__(self,

                 x: int | Percentage,
                 y: int | Percentage,
                 width: int | Percentage,
                 height: int | Percentage,
                 ):

        self._x = x
        self._y = y
        self._width = width
        self._height = height

        self._window_width = 0
        self._window_height = 0

    # getter / setter

    @property
    def x(self) -> int:
        return self._x if isinstance(self._x, int) else self._x * self._window_width

    @x.setter
    def x(self, x: int | Percentage) -> None:
        self._x = x

    @property
    def y(self) -> int:
        return self._y if isinstance(self._y, int) else self._y * self._window_height

    @y.setter
    def y(self, y: int | Percentage) -> None:
        self._y = y

    @property
    def width(self) -> int:
        return self._width if isinstance(self._width, int) else self._width * self._window_width

    @width.setter
    def width(self, width: int | Percentage) -> None:
        self._width = width

    @property
    def height(self) -> int:
        return self._height if isinstance(self._height, int) else self._height * self._window_height

    @height.setter
    def height(self, height: int | Percentage) -> None:
        self._height = height

    @property
    def bbox(self) -> BBox:
        return self.x, self.y, self.x + self.width, self.y + self.height

    def on_resize(self, window: "Window", scene: "Scene", width: int, height: int):
        self._window_width = width
        self._window_height = height
