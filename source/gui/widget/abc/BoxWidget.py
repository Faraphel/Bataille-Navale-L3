from abc import ABC
from typing import TYPE_CHECKING, Optional

from source.gui.widget.abc import Widget
from source.type import Percentage
from source.utils import in_bbox

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

        self._hovering = False  # is the button currently hovered ?
        self._clicking = False  # is the button currently clicked ?

    # property

    @property
    def x(self) -> int:
        return self.scene.window.width * self._p_x

    @x.setter
    def x(self, x: Percentage):
        self._p_x = x

    @property
    def y(self) -> int:
        return self.scene.window.height * self._p_y

    @y.setter
    def y(self, y: Percentage):
        self._p_y = y

    @property
    def width(self) -> int:
        return None if self._p_width is None else self.scene.window.width * self._p_width

    @width.setter
    def width(self, width: Optional[Percentage]):
        self._p_width = width

    @property
    def height(self) -> int:
        return None if self._p_height is None else self.scene.window.height * self._p_height

    @height.setter
    def height(self, height: Optional[Percentage]):
        self._p_height = height

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
        if not in_bbox((x, y), self.bbox): return

        self.clicking = True

        self.on_press(button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        old_click: bool = self._clicking
        self.clicking = False

        if not in_bbox((x, y), self.bbox): return

        # if this button was the one hovered when the click was pressed
        if old_click: self.on_release(button, modifiers)

    def on_press(self, button: int, modifiers: int):
        """
        This event is called when the bbox is pressed
        """

    def on_release(self, button: int, modifiers: int):
        """
        This event is called when the bbox is released
        """