from typing import TYPE_CHECKING

import pyglet.clock

from source.gui import texture, widget, sound
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
            image=texture.Result.Style1.get("victory" if won else "defeat")
        )

        sound.Game.get("won" if won else "loose").play()

        # TODO: rendre l'image transparente si possible

        from source.gui.scene import MainMenu
        pyglet.clock.schedule_once(lambda dt: self.window.set_scene(MainMenu), 5.0)
