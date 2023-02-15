from typing import TYPE_CHECKING

import pyglet

from source.gui.scene.abc import Scene
from source.gui.widget import Checkbox

if TYPE_CHECKING:
    from source.gui.window import Window


class Settings(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        texture_tick_disabled = pyglet.image.load("./assets/image/checkbox/disabled.png")
        texture_tick_enabled = pyglet.image.load("./assets/image/checkbox/enabled.png")

        self.checkbox = self.add_widget(
            Checkbox,

            x=0.45, y=0.45, width=0.1, height=0.1,

            texture_disabled=texture_tick_disabled,
            texture_enabled=texture_tick_enabled,
        )

    def on_draw(self):
        self.checkbox.draw()
