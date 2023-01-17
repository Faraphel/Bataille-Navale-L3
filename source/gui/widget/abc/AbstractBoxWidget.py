from abc import ABC

from source.gui.widget.abc import AbstractWidget
from source.type import BBox


class AbstractBoxWidget(AbstractWidget, ABC):
    def __init__(self, x: int, y: int, width: int, height: int):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    # getter and setter, allow subclass to react when one of these value is changed

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        self._y = y

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        self._height = height

    @property
    def bbox(self) -> BBox:
        return self.x, self.y, self.x + self.width, self.y + self.height
