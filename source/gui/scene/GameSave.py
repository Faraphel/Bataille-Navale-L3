from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.scene.abc.Popup import Popup
from source.network.packet import PacketResponseSave

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.scene import Game


class GameSave(Popup):
    def __init__(self, window: "Window", game_scene: "Game", **kwargs):
        super().__init__(window, **kwargs)

        self.game_scene = game_scene

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=1.0, height=1.0,

            image=texture.Popup.Style1.background
        )

        self.text = self.add_widget(
            widget.Text,

            x=0.5, y=0.5,

            anchor_x="center",

            text="L'adversaire souhaite sauvegarder",
            font_size=28,
            align="center",
        )

        self.refuse = self.add_widget(
            widget.Button,
            x=0.20, y=0.20, width=0.2, height=0.1,

            label_text="Refuser",

            style=texture.Button.Style1
        )

        self.refuse.add_listener("on_click_release", lambda *_: self.choose_save(value=False))

        self.accept = self.add_widget(
            widget.Button,
            x=0.60, y=0.20, width=0.2, height=0.1,

            label_text="Accepter",

            style=texture.Button.Style1
        )

        self.accept.add_listener("on_click_release", lambda *_: self.choose_save(value=True))

    def choose_save(self, value: bool):
        PacketResponseSave(value=value).send_connection(self.game_scene.connection)
        self.window.remove_scene(self)
        self.game_scene.save(value=value)

