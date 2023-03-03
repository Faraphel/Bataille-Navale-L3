from abc import ABC

from source.gui.event import StopEvent
from source.gui.scene.abc import Scene


class Popup(Scene, ABC):
    """
    Similaire à une Scène, mais empêche les interactions avec les scènes en arrière-plan.
    """

    def on_mouse_press_after(self, x: int, y: int, button: int, modifiers: int):
        raise StopEvent()

    def on_mouse_motion_after(self, x: int, y: int, button: int, modifiers: int):
        raise StopEvent()
