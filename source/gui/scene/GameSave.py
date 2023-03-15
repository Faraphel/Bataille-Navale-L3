from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import vh_full, vw_full, vw, vh
from source.gui.scene.abc.Popup import Popup
from source.network.packet import PacketResponseSave

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.scene import Game


class GameSave(Popup):
    """
    Cette scène affiche une proposition de sauvegarde de la partie
    """

    def __init__(self, window: "Window", game_scene: "Game", **kwargs):
        super().__init__(window, **kwargs)

        self.game_scene = game_scene

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=vw_full, height=vh_full,

            image=texture.Popup.Style1.background
        )

        self.text = self.add_widget(
            widget.Text,

            x=50*vw, y=50*vh,

            anchor_x="center",

            text="L'adversaire souhaite sauvegarder",
            font_size=28,
            align="center",
        )

        self.refuse = self.add_widget(
            widget.Button,
            x=20*vw, y=20*vh, width=20*vw, height=10*vh,

            label_text="Refuser",

            style=texture.Button.Style1
        )

        self.refuse.add_listener("on_click_release", lambda *_: self.choose_save(value=False))

        self.accept = self.add_widget(
            widget.Button,
            x=60*vw, y=20*vh, width=20*vw, height=10*vh,

            label_text="Accepter",

            style=texture.Button.Style1
        )

        self.accept.add_listener("on_click_release", lambda *_: self.choose_save(value=True))

    def choose_save(self, value: bool):
        PacketResponseSave(value=value).send_connection(self.game_scene.connection)
        self.window.remove_scene(self)
        self.game_scene.save(value=value)

