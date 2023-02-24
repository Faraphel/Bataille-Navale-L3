from typing import TYPE_CHECKING

import pyglet.clock

from source.gui import texture, widget
from source.gui.scene.abc import Scene

if TYPE_CHECKING:
    from source.gui.window import Window


class Result(Scene):
    def __init__(self, window: "Window", won: bool, **kwargs):
        super().__init__(window, **kwargs)

        self.image = self.add_widget(
            widget.Image,

            x=0, y=0, width=1.0, height=1.0,
            image=texture.Result.Style1.victory if won else texture.Result.Style1.defeat
        )

        from source.gui.scene import MainMenu
        pyglet.clock.schedule_once(lambda dt: self.window.set_scene(MainMenu), 5.0)

    def on_draw(self):
        self.image.draw()
