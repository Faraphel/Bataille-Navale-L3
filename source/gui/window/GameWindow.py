import pyglet.window

from source.gui.window import Window
from source.type import ColorRGBA


class GameWindow(Window):  # NOQA
    """
    Similar to the normal Window, but add small feature useful for a game like a fps counter.
    """

    def __init__(self,

                 fps_color: ColorRGBA = (255, 255, 255, 200),
                 fps_enable: bool = True,

                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._fps_counter = pyglet.window.FPSDisplay(self, color=fps_color)
        self.fps_enable = fps_enable

    def on_draw_after(self):
        if self.fps_enable: self._fps_counter.draw()
