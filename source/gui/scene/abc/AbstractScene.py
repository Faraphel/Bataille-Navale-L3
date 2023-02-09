from abc import ABC
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.widget.abc import AbstractWidget


class AbstractScene(ABC):
    """
    An abstract scene that can be attached to a window.
    Can be used to create a menu, an overlay, ...
    """

    def __init__(self, window: "Window"):
        self._widgets: list["AbstractWidget"] = []  # the lists of the widgets in the scene
        self._window: "Window" = window  # the window where the scene is attached

    # widget

    def add_widget(self, *widgets: "AbstractWidget", priority: int = 0) -> None:
        for widget in widgets:
            self._widgets.insert(priority, widget)
            widget.on_scene_added(self)

    def remove_widget(self, *widgets: "AbstractWidget") -> None:
        for widget in widgets:
            widget.on_scene_removed(self)
            self._widgets.remove(widget)

    def clear_widget(self) -> None:
        self.remove_widget(*self._widgets)

