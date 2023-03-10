from typing import TYPE_CHECKING

import pyglet.clock

from source.gui import texture, widget, media
from source.gui.position import vw_full, vh_full
from source.gui.scene.abc.Popup import Popup

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.scene import Game


class GameResult(Popup):
    def __init__(self, window: "Window", game_scene: "Game", won: bool, **kwargs):
        super().__init__(window, **kwargs)

        self.game_scene = game_scene

        self.image = self.add_widget(
            widget.Image,

            x=0, y=0, width=vw_full, height=vh_full,
            image=texture.Result.Style1.get("victory" if won else "defeat")
        )

        from source.gui.scene import MainMenu
        pyglet.clock.schedule_once(lambda dt: self.window.set_scene(MainMenu), 5.0)
