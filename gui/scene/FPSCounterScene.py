from typing import Optional

import pyglet

from gui.scene import Scene
from gui.window import Window


class FPSCounterScene(Scene):
    """
    This scene represent a simple FPS Counter.
    """

    def __init__(self):
        self.fps_display: Optional[pyglet.window.FPSDisplay] = None

    def on_window_added(self, window: Window):
        # the fps display need to be defined here because it is the moment where the window is first accessible
        self.fps_display = pyglet.window.FPSDisplay(window=window)

    def on_draw(self, window: Window) -> None:
        self.fps_display.draw()
