from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.widget.base import BaseWidget


class BaseScene:
    """
    A scene that can be attached to a window
    """

    def __init__(self):
        self._widgets: list["BaseWidget"] = []
        self._window: Optional["Window"] = None

    # widget

    def add_widget(self, *widgets: "BaseWidget", priority: int = 0) -> None:
        for widget in widgets:
            self._widgets.insert(priority, widget)
            widget.on_scene_added(self)

    def remove_widget(self, *widgets: "BaseWidget") -> None:
        for widget in widgets:
            widget.on_scene_removed(self)
            self._widgets.remove(widget)

    def clear_widget(self) -> None:
        self.remove_widget(*self._widgets)

    # scene event

    def on_window_added(self, window: "Window"):  # when the Scene is added to a window
        for widget in self._widgets: widget.on_window_added(window, self)

    def on_window_removed(self, window: "Window"):  # when the Scene is removed from a window
        for widget in self._widgets: widget.on_window_removed(window, self)

    # window

    @property
    def window(self) -> "Window":
        return self._window

    @window.setter
    def window(self, window: "Window"):
        if self._window is not None: self.on_window_removed(self._window)
        self._window = window
        if self._window is not None: self.on_window_added(self._window)

    # event

    def on_draw(self, window: "Window"):
        for widget in self._widgets: widget.on_draw(window, self)

    def on_resize(self, window: "Window", width: int, height: int):
        for widget in self._widgets: widget.on_resize(window, self, width, height)

    def on_hide(self, window: "Window"):
        for widget in self._widgets: widget.on_hide(window, self)

    def on_show(self, window: "Window"):
        for widget in self._widgets: widget.on_show(window, self)

    def on_close(self, window: "Window"):
        for widget in self._widgets: widget.on_close(window, self)

    def on_expose(self, window: "Window"):
        for widget in self._widgets: widget.on_expose(window, self)

    def on_activate(self, window: "Window"):
        for widget in self._widgets: widget.on_activate(window, self)

    def on_deactivate(self, window: "Window"):
        for widget in self._widgets: widget.on_deactivate(window, self)

    def on_text(self, window: "Window", char: str):
        for widget in self._widgets: widget.on_text(window, self, char)

    def on_move(self, window: "Window", x: int, y: int):
        for widget in self._widgets: widget.on_move(window, self, x, y)

    def on_context_lost(self, window: "Window"):
        for widget in self._widgets: widget.on_context_lost(window, self)

    def on_context_state_lost(self, window: "Window"):
        for widget in self._widgets: widget.on_context_state_lost(window, self)

    def on_key_press(self, window: "Window", symbol: int, modifiers: int):
        for widget in self._widgets: widget.on_key_press(window, self, symbol, modifiers)

    def on_key_release(self, window: "Window", symbol: int, modifiers: int):
        for widget in self._widgets: widget.on_key_release(window, self, symbol, modifiers)

    def on_key_held(self, window: "Window", dt: float, symbol: int, modifiers: int):
        for widget in self._widgets: widget.on_key_held(window, self, dt, symbol, modifiers)

    def on_mouse_enter(self, window: "Window", x: int, y: int):
        for widget in self._widgets: widget.on_mouse_enter(window, self, x, y)

    def on_mouse_leave(self, window: "Window", x: int, y: int):
        for widget in self._widgets: widget.on_mouse_leave(window, self, x, y)

    def on_text_motion(self, window: "Window", motion: int):
        for widget in self._widgets: widget.on_text_motion(window, self, motion)

    def on_text_motion_select(self, window: "Window", motion: int):
        for widget in self._widgets: widget.on_text_motion_select(window, self, motion)

    def on_mouse_motion(self, window: "Window", x: int, y: int, dx: int, dy: int):
        for widget in self._widgets: widget.on_mouse_motion(window, self, x, y, dx, dy)

    def on_mouse_press(self, window: "Window", x: int, y: int, button: int, modifiers: int):
        for widget in self._widgets: widget.on_mouse_press(window, self, x, y, button, modifiers)

    def on_mouse_release(self, window: "Window", x: int, y: int, button: int, modifiers: int):
        for widget in self._widgets: widget.on_mouse_release(window, self, x, y, button, modifiers)

    def on_mouse_drag(self, window: "Window", x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        for widget in self._widgets: widget.on_mouse_drag(window, self, x, y, dx, dy, buttons, modifiers)

    def on_mouse_scroll(self, window: "Window", x: int, y: int, scroll_x: float, scroll_y: float):
        for widget in self._widgets: widget.on_mouse_scroll(window, self, x, y, scroll_x, scroll_y)
