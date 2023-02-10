from source.gui.widget.abc import Widget

from typing import TYPE_CHECKING

import pyglet

if TYPE_CHECKING:
    from source.gui.scene import Scene


class FPSDisplay(Widget):
    """
    A widget that display the current FPS of the scene's window
    """

    def __init__(self, scene: "Scene"):
        super().__init__(scene)

        self.fps_display = pyglet.window.FPSDisplay(scene.window)

    def on_draw(self):
        self.fps_display.draw()
