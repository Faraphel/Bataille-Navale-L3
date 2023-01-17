from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.gui.scene.abc import AbstractScene
    from source.gui.window import Window


class AbstractWidget(ABC):
    """
    This class represent a widget that can be attached to a Scene.

    It can be used to create a button, a label, ...
    """

    # widget event

    def on_scene_added(self, scene: "AbstractScene"): pass
    def on_scene_removed(self, scene: "AbstractScene"): pass

    # scene event

    def on_window_added(self, window: "Window", scene: "AbstractScene"): pass
    def on_window_removed(self, window: "Window", scene: "AbstractScene"): pass

    # global event

    def on_draw(self, window: "Window", scene: "AbstractScene"): pass
    def on_resize(self, window: "Window", scene: "AbstractScene", width: int, height: int): pass
    def on_hide(self, window: "Window", scene: "AbstractScene"): pass
    def on_show(self, window: "Window", scene: "AbstractScene"): pass
    def on_close(self, window: "Window", scene: "AbstractScene"): pass
    def on_expose(self, window: "Window", scene: "AbstractScene"): pass
    def on_activate(self, window: "Window", scene: "AbstractScene"): pass
    def on_deactivate(self, window: "Window", scene: "AbstractScene"): pass
    def on_text(self, window: "Window", scene: "AbstractScene", char: str): pass
    def on_move(self, window: "Window", scene: "AbstractScene", x: int, y: int): pass
    def on_context_lost(self, window: "Window", scene: "AbstractScene"): pass
    def on_context_state_lost(self, window: "Window", scene: "AbstractScene"): pass
    def on_key_press(self, window: "Window", scene: "AbstractScene", symbol: int, modifiers: int): pass
    def on_key_release(self, window: "Window", scene: "AbstractScene", symbol: int, modifiers: int): pass
    def on_key_held(self, window: "Window", scene: "AbstractScene", dt: float, symbol: int, modifiers: int): pass
    def on_mouse_enter(self, window: "Window", scene: "AbstractScene", x: int, y: int): pass
    def on_mouse_leave(self, window: "Window", scene: "AbstractScene", x: int, y: int): pass
    def on_text_motion(self, window: "Window", scene: "AbstractScene", motion: int): pass
    def on_text_motion_select(self, window: "Window", scene: "AbstractScene", motion: int): pass
    def on_mouse_motion(self, window: "Window", scene: "AbstractScene", x: int, y: int, dx: int, dy: int): pass
    def on_mouse_press(self, window: "Window", scene: "AbstractScene", x: int, y: int, button: int, modifiers: int): pass
    def on_mouse_release(self, window: "Window", scene: "AbstractScene", x: int, y: int, button: int, modifiers: int): pass
    def on_mouse_drag(self, window: "Window", scene: "AbstractScene", x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int): pass
    def on_mouse_scroll(self, window: "Window", scene: "AbstractScene", x: int, y: int, scroll_x: float, scroll_y: float): pass
