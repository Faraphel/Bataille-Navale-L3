import pyglet.event

from gui.window import Window


class Scene(pyglet.event.EventDispatcher):
    """
    This class represent a scene that can be applied to a pyglet window.

    The scene can represent anything like the main menu, the game, the
    options' menu, the multiplayer menu, ...
    """

    def on_window_added(self, window: Window): pass  # when the Scene is added to a window
    def on_window_removed(self, window: Window): pass  # when the Scene is removed from a window

    def on_draw(self, window: Window): pass
    def on_resize(self, window: Window, width: int, height: int): pass
    def on_hide(self, window: Window): pass
    def on_show(self, window: Window): pass
    def on_close(self, window: Window): pass
    def on_expose(self, window: Window): pass
    def on_activate(self, window: Window): pass
    def on_deactivate(self, window: Window): pass
    def on_text(self, window: Window, char: str): pass
    def on_move(self, window: Window, x: int, y: int): pass
    def on_context_lost(self, window: Window): pass
    def on_context_state_lost(self, window: Window): pass
    def on_key_press(self, window: Window, symbol: int, modifiers: int): pass
    def on_key_release(self, window: Window, symbol: int, modifiers: int): pass
    def on_key_held(self, window: Window, dt: float, symbol: int, modifiers: int): pass
    def on_mouse_enter(self, window: Window, x: int, y: int): pass
    def on_mouse_leave(self, window: Window, x: int, y: int): pass
    def on_text_motion(self, window: Window, motion: int): pass
    def on_text_motion_select(self, window: Window, motion: int): pass
    def on_mouse_motion(self, window: Window, x: int, y: int, dx: int, dy: int): pass
    def on_mouse_press(self, window: Window, x: int, y: int, button: int, modifiers: int): pass
    def on_mouse_release(self, window: Window, x: int, y: int, button: int, modifiers: int): pass
    def on_mouse_drag(self, window: Window, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int): pass
    def on_mouse_scroll(self, window: Window, x: int, y: int, scroll_x: float, scroll_y: float): pass



