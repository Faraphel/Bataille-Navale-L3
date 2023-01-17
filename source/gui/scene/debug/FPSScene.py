from typing import TYPE_CHECKING, Optional

import pyglet.window

from source.gui.scene.abc import AbstractScene

if TYPE_CHECKING:
    from source.gui.window import Window


class FPSAbstractScene(AbstractScene):
    """
    A base scene that can be used as an overlay to display the FPS
    """

    def __init__(self):
        super().__init__()
        self._fps_display: Optional[pyglet.window.FPSDisplay] = None

    def on_window_added(self, window: "Window"):
        self._fps_display = pyglet.window.FPSDisplay(window)

    def on_draw(self, window: "Window"):
        self._fps_display.draw()
