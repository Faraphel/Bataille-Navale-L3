from typing import TYPE_CHECKING

import pyglet.clock

from source.gui import texture, widget
from source.gui.event import StopEvent
from source.gui.scene.abc import Scene
from source.gui.scene.abc.Popup import Popup

if TYPE_CHECKING:
    from source.gui.window import Window


class Result(Popup):
    def __init__(self, window: "Window", won: bool, **kwargs):
        super().__init__(window, **kwargs)

        self.image = self.add_widget(
            widget.Image,

            x=0, y=0, width=1.0, height=1.0,
            image=texture.Result.Style1.victory if won else texture.Result.Style1.defeat
        )

        # TODO: rendre l'image transparente si possible

        from source.gui.scene import MainMenu
        pyglet.clock.schedule_once(lambda dt: self.window.set_scene(MainMenu), 5.0)
