from typing import TYPE_CHECKING

import pyglet.window

from source.gui.scene.base import BaseScene

if TYPE_CHECKING:
    from source.gui.window import Window


class FPSScene(BaseScene):
    def __init__(self):
        super().__init__()
        self._fps_display = None

    def on_window_added(self, window: "Window"):
        self._fps_display = pyglet.window.FPSDisplay(window)

    def on_draw(self, window: "Window"):
        self._fps_display.draw()
