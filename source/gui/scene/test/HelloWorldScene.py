from datetime import datetime, timedelta

import pyglet

from source.gui.scene.base import Scene

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.gui.window import Window


class HelloWorldScene(Scene):
    """
    This scene is a simple Hello World.

    You can type anything with the keyboard or use backspace to remove characters.
    The text is centered on the screen.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = pyglet.text.Label(
            "Hello World !",
            anchor_x="center",
            anchor_y="center"
        )

        # remember the cooldown for the backspace button
        self._hold_backspace_last_call: datetime = datetime.now()

    def on_draw(self, window: "Window") -> None:
        super().on_draw(window)

        self.label.draw()

    def on_resize(self, window: "Window", width: int, height: int) -> None:
        super().on_resize(window, width, height)

        self.label.x = width // 2
        self.label.y = height // 2

    def on_text(self, window: "Window", char: str):
        super().on_text(window, char)

        self.label.text += char

    def on_key_held(self, window: "Window", dt: float, symbol: int, modifiers: int):
        super().on_key_held(window, dt, symbol, modifiers)

        if symbol == pyglet.window.key.BACKSPACE:

            # add a cooldown of 0.1 second on the backspace key
            now = datetime.now()
            if self._hold_backspace_last_call + timedelta(seconds=0.1) < now:
                self._hold_backspace_last_call = now

                self.label.text = self.label.text[:-1]
