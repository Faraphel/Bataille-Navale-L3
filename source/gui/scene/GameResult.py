from typing import TYPE_CHECKING

import pyglet.clock

from source.gui import texture, widget
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

            x=0, y=0, width=1.0, height=1.0,
            image=texture.Result.Style1.victory if won else texture.Result.Style1.defeat
        )

        # TODO: rendre l'image transparente si possible

        pyglet.clock.schedule_once(lambda dt: self.game_scene.quit, 5.0)
