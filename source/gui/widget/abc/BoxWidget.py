from abc import ABC
from typing import TYPE_CHECKING, Optional

from source.gui.widget.abc import Widget
from source.type import Percentage

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class BoxWidget(Widget, ABC):
    """
    Same as a basic widget, but represent a box
    """

    def __init__(self, scene: "Scene",
                 x: Percentage = 0,
                 y: Percentage = 0,
                 width: Percentage = None,
                 height: Percentage = None):
        super().__init__(scene)

        # memorize the value with a percent value
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def x(self):
        return self.scene.window.width * self._p_x

    @x.setter
    def x(self, x: Percentage):
        self._p_x = x

    @property
    def y(self):
        return self.scene.window.height * self._p_y

    @y.setter
    def y(self, y: Percentage):
        self._p_y = y

    @property
    def width(self):
        return None if self._p_width is None else self.scene.window.width * self._p_width

    @width.setter
    def width(self, width: Optional[Percentage]):
        self._p_width = width

    @property
    def height(self):
        return None if self._p_height is None else self.scene.window.height * self._p_height

    @height.setter
    def height(self, height: Optional[Percentage]):
        self._p_height = height

    @property
    def xy(self):
        return self.x, self.y

    @property
    def size(self):
        return self.width, self.height

    @property
    def bbox(self):
        return self.x, self.y, self.width, self.height
