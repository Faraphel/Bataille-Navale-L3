from abc import ABC
from typing import TYPE_CHECKING, Optional

from source.gui.widget.abc import Widget
from source.type import Distance, Point2D
from source.utils import in_bbox

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class BoxWidget(Widget, ABC):
    """
    Same as a basic widget, but inside a box
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

        self.hovering = False  # is the button currently hovered ?
        self.clicking = False  # is the button currently clicked ?
        self.activated = False  # is the button activated ? (the last click was inside this widget)

    # property

    def _getter_distance(self, raw_distance: Distance) -> int:
        """
        Return the true distance in pixel from a more abstract distance
        :param raw_distance: the distance object to convert to pixel
        :return: the true distance in pixel
        """

        if isinstance(raw_distance, int): return raw_distance
        if callable(raw_distance): return raw_distance(self)
        if raw_distance is None: return 0

        raise TypeError(f"Invalid type for the distance : {type(raw_distance)}")

    @property
    def x(self) -> int:
        return self._getter_distance(self._x)

    @x.setter
    def x(self, x: Distance):
        self._x = x

    @property
    def y(self) -> int:
        return self._getter_distance(self._y)

    @y.setter
    def y(self, y: Distance):
        self._y = y

    @property
    def xy(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def x2(self) -> int:
        return self.x + self.width

    @property
    def y2(self) -> int:
        return self.y + self.height

    @property
    def xy2(self) -> tuple[int, int]:
        return self.x2, self.y2

    @property
    def width(self) -> int:
        return self._getter_distance(self._width)

    @width.setter
    def width(self, width: Optional[Distance]):
        self._width = width

    @property
    def height(self) -> int:
        return self._getter_distance(self._height)

    @height.setter
    def height(self, height: Optional[Distance]):
        self._height = height

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    @property
    def bbox(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.x2, self.y2

    @property
    def center_x(self) -> float:
        return self.x + (self.width / 2)

    @property
    def center_y(self) -> float:
        return self.y + (self.height / 2)

    @property
    def center(self) -> tuple[float, float]:
        return self.center_x, self.center_y

    # function

    def in_bbox(self, point: Point2D) -> bool:
        return in_bbox(point, self.bbox)

    # event

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """
        When the mouse is moved, this event is triggered.
        Allow the implementation of the on_hover_enter and on_hover_leave events
        :x: the x position of the mouse
        :y: the y position of the mouse
        :dx: the difference of the x mouse axis
        :dy: the difference of the y mouse axis
        """

        rel_x, rel_y = x - self.x, y - self.y

        old_hovering = self.hovering
        self.hovering = self.in_bbox((x, y))

        if old_hovering != self.hovering:  # if the hover changed
            # call the hover changed event
            self.trigger_event("on_hover_change", rel_x, rel_y)
            # call the hover enter / leave event
            self.trigger_event("on_hover_enter" if self.hovering else "on_hover_leave", rel_x, rel_y)

        if self.hovering:  # if the mouse motion is inside the collision
            self.trigger_event("on_hover", rel_x, rel_y)  # call the hover event

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        rel_x, rel_y = x - self.x, y - self.y

        self.activated = self.in_bbox((x, y))
        self.trigger_event("on_activate_change", rel_x, rel_y, button, modifiers)

        if self.activated:  # if the click was inside the widget
            self.trigger_event("on_activate_enter", rel_x, rel_y, button, modifiers)

            self.clicking = True  # the widget is also now clicked
            self.trigger_event("on_click_change", rel_x, rel_y, button, modifiers)
            self.trigger_event("on_click_press", rel_x, rel_y, button, modifiers)

        else:
            self.trigger_event("on_activate_leave", rel_x, rel_y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        rel_x, rel_y = x - self.x, y - self.y

        old_click: bool = self.clicking
        self.clicking = False  # the widget is no longer clicked

        if not self.in_bbox((x, y)): return  # if the release was not in the collision, ignore

        if old_click:  # if this button was the one hovered when the click was pressed
            self.trigger_event("on_click_change", rel_x, rel_y, button, modifiers)
            self.trigger_event("on_click_release", rel_x, rel_y, button, modifiers)
