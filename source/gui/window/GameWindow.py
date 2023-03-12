from pathlib import Path

import pyglet.window

from source.gui.window import Window
from source.option import Option
from source.type import ColorRGBA


class GameWindow(Window):  # NOQA
    """
    Similar to the normal Window, but add small feature useful for a game like a fps counter.
    """

    def __init__(self,

                 option_path: Path = None,

                 fps_color: ColorRGBA = (255, 255, 255, 200),
                 fps_enable: bool = False,

                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._fps_counter = pyglet.window.FPSDisplay(self, color=fps_color)
        self._fps_enable = fps_enable

        self.option = None

        try:
            if option_path.exists():
                self.option = Option.load(self, option_path)
        except Exception:  # NOQA
            pass

        if self.option is None:
            self.option = Option(window=self)

    @property
    def fps_enable(self) -> bool:
        return self._fps_enable

    def set_fps_enabled(self, value: bool):
        self._fps_enable = value

    def on_draw_after(self):
        if self._fps_enable: self._fps_counter.draw()
