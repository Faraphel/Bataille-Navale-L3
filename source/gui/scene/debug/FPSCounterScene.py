from typing import Optional, TYPE_CHECKING

import pyglet

from source.gui.scene.base import Scene

if TYPE_CHECKING:
    from source.gui.window import Window


class FPSCounterScene(Scene):
    """
    This scene represent a simple FPS Counter.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fps_display: Optional[pyglet.window.FPSDisplay] = None

    def on_window_added(self, window: "Window"):
        super().on_window_added(window)

        # the fps display need to be defined here because it is the moment where the window is first accessible
        self.fps_display = pyglet.window.FPSDisplay(window=window)

    def on_draw(self, window: "Window") -> None:
        super().on_draw(window)

        self.fps_display.draw()
