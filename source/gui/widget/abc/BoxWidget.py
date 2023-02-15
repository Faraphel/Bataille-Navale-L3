from abc import ABC
from typing import TYPE_CHECKING, Optional

from source.gui.widget.abc import Widget
from source.type import Distance, Percentage
from source.utils import in_bbox

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class BoxWidget(Widget, ABC):
    """
    Same as a basic widget, but represent a box
    """

    def __init__(self, scene: "Scene",
                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None):
        super().__init__(scene)

        # memorize the value with a percent value
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self._hovering = False  # is the button currently hovered ?
        self._clicking = False  # is the button currently clicked ?
        self._activated = False  # is the button activated ? (the last click was inside this widget)

    # property

    def _getter_distance(self, max_distance: int, raw_distance: Distance) -> int:
        """
        Return the true distance in pixel from a more abstract distance
        :param max_distance: the max value the distance in pixel should have
        :param raw_distance: the distance object to convert to pixel
        :return: the true distance in pixel
        """

        if isinstance(raw_distance, Percentage): return int(max_distance * raw_distance)
        if isinstance(raw_distance, int): return raw_distance
        if callable(raw_distance): return raw_distance(self)
        if raw_distance is None: return 0

        raise TypeError(f"Invalid type for the distance : {type(raw_distance)}")

    @property
    def x(self) -> int:
        return self._getter_distance(self.scene.window.width, self._x)

    @x.setter
    def x(self, x: Distance):
        self._x = x

    @property
    def y(self) -> int:
        return self._getter_distance(self.scene.window.height, self._y)

    @y.setter
    def y(self, y: Distance):
        self._y = y

    @property
    def width(self) -> int:
        return self._getter_distance(self.scene.window.width, self._width)

    @width.setter
    def width(self, width: Optional[Distance]):
        self._width = width

    @property
    def height(self) -> int:
        return self._getter_distance(self.scene.window.height, self._height)

    @height.setter
    def height(self, height: Optional[Distance]):
        self._height = height

    @property
    def xy(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    @property
    def bbox(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.x + self.width, self.y + self.height

    # property that can be used to add event when these value are modified in some specific widget.

    @property
    def hovering(self):
        return self._hovering

    @hovering.setter
    def hovering(self, hovering: bool):
        self._hovering = hovering

    @property
    def clicking(self):
        return self._clicking

    @clicking.setter
    def clicking(self, clicking: bool):
        self._clicking = clicking

    @property
    def activated(self):
        return self._activated

    @activated.setter
    def activated(self, activated: bool):
        self._activated = activated

    # event

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):  # NOQA
        """
        When the mouse is moved, this event is triggered.
        Allow the implementation of the on_hover_enter and on_hover_leave events
        :x: the x position of the mouse
        :y: the y position of the mouse
        :dx: the difference of the x mouse axis
        :dy: the difference of the y mouse axis
        """

        old_hovering = self.hovering
        self.hovering = in_bbox((x, y), self.bbox)

        if old_hovering != self.hovering:  # if the hover changed
            if self.hovering: self.on_hover_enter()  # call the hover enter event
            else: self.on_hover_leave()  # call the hover leave event

    def on_hover_enter(self):
        """
        This event is called when the mouse enter the bbox of the widget
        """

    def on_hover_leave(self):
        """
        This event is called when the mouse leave the bbox of the widget
        """

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        # if this button was the one hovered when the click was pressed

        if not in_bbox((x, y), self.bbox):
            self.activated = False  # if the click was not in the bbox, disable the activated state
            return

        self.activated = True  # if the click is inside the bbox, enable the activated state
        self.clicking = True  # the widget is now clicked

        self.on_pressed(x - self.x, y - self.y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        old_click: bool = self._clicking
        self.clicking = False  # the widget is no longer clicked

        if not in_bbox((x, y), self.bbox): return

        # if this button was the one hovered when the click was pressed
        if old_click: self.on_release(x - self.x, y - self.y, button, modifiers)

    def on_pressed(self, rel_x: int, rel_y: int, button: int, modifiers: int):
        """
        This event is called when the bbox is pressed
        """

    def on_release(self, rel_x: int, rel_y: int, button: int, modifiers: int):
        """
        This event is called when the bbox is released
        """