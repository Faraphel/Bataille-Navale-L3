from typing import Optional

import pyglet.window

from gui.scene import Scene


class Window(pyglet.window.Window):  # NOQA - pycharm think pyglet window is abstract
    """
    This class represent a Window based on the pyglet Window object.

    Allow to use a "Scene" system to create very different interface like
    a main menu, options menu, ... that can overlay each other without
    putting everything in the window code.
    """

    def __init__(self, *args, scenes: Optional[Scene] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._scenes: list[Scene] = [] if scenes is None else scenes

        # add a keys handler to the window
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

    # scene methods

    def set_scene(self, scene: Scene) -> None:
        """
        Set the scene of the window
        :param scene: the scene to set
        """
        self._scenes = [scene]
        scene.on_window_added(self)

    def clear_scene(self) -> None:
        """
        Clear all the scenes of the window
        """
        for scene in self._scenes: scene.on_window_removed(self)
        self._scenes.clear()

    def add_scene(self, scene: Scene, priority: int = 0) -> None:
        """
        Add a scene to the window
        :param scene: the scene to add
        :param priority: the priority level of the scene. The higher, the more the scene will be drawn on top
        """
        self._scenes.insert(priority, scene)
        scene.on_window_added(self)

    def remove_scene(self, scene: Scene) -> None:
        """
        Remove a scene from the window
        :param scene: the scene to remove
        """
        scene.on_window_removed(self)
        self._scenes.remove(scene)

    # window event methods

    # NOTE: it is too difficult to refactor all the event because :
    #     - There is no event "on_any_event" or equivalent
    #     - The list of all the event is not available in the source
    #     - Some event need special code like on_draw with the clear, on_resize with the super, ...

    def on_draw(self):  # NOQA
        self.clear()  # clear the window to reset it
        for scene in self._scenes: scene.on_draw(self)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)  # this function is already defined and used
        for scene in self._scenes: scene.on_resize(self, width, height)

    def on_hide(self):
        for scene in self._scenes: scene.on_hide(self)

    def on_show(self):
        for scene in self._scenes: scene.on_show(self)

    def on_close(self):
        super().close()  # this function is already defined and used
        for scene in self._scenes: scene.on_close(self)

    def on_expose(self):
        for scene in self._scenes: scene.on_expose(self)

    def on_activate(self):
        for scene in self._scenes: scene.on_activate(self)

    def on_deactivate(self):
        for scene in self._scenes: scene.on_deactivate(self)

    def on_text(self, char: str):
        for scene in self._scenes: scene.on_text(self, char)

    def on_move(self, x: int, y: int):
        for scene in self._scenes: scene.on_move(self, x, y)

    def on_context_lost(self):
        for scene in self._scenes: scene.on_context_lost(self)

    def on_context_state_lost(self):
        for scene in self._scenes: scene.on_context_state_lost(self)

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)  # this function is already defined and used
        for scene in self._scenes: scene.on_key_press(self, symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        for scene in self._scenes: scene.on_key_release(self, symbol, modifiers)

    def on_mouse_enter(self, x: int, y: int):
        for scene in self._scenes: scene.on_mouse_enter(self, x, y)

    def on_mouse_leave(self, x: int, y: int):
        for scene in self._scenes: scene.on_mouse_leave(self, x, y)

    def on_text_motion(self, motion: int):
        for scene in self._scenes: scene.on_text_motion(self, motion)

    def on_text_motion_select(self, motion: int):
        for scene in self._scenes: scene.on_text_motion_select(self, motion)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        for scene in self._scenes: scene.on_mouse_motion(self, x, y, dx, dy)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        for scene in self._scenes: scene.on_mouse_press(self, x, y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        for scene in self._scenes: scene.on_mouse_release(self, x, y, button, modifiers)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        for scene in self._scenes: scene.on_mouse_drag(self, x, y, dx, dy, buttons, modifiers)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: float, scroll_y: float):
        for scene in self._scenes: scene.on_mouse_scroll(self, x, y, scroll_x, scroll_y)
