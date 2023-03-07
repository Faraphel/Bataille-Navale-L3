from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import h_full, w_full, w_percent, h_percent
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

            x=0, y=0, width=w_full, height=h_full,

            image=texture.Popup.Style1.background
        )

        self.text = self.add_widget(
            widget.Text,

            x=w_percent(50), y=h_percent(50),

            anchor_x="center",

            text="L'adversaire souhaite sauvegarder",
            font_size=28,
            align="center",
        )

        self.refuse = self.add_widget(
            widget.Button,
            x=w_percent(20), y=h_percent(20), width=w_percent(20), height=h_percent(10),

            label_text="Refuser",

            style=texture.Button.Style1
        )

        self.refuse.add_listener("on_click_release", lambda *_: self.choose_save(value=False))

        self.accept = self.add_widget(
            widget.Button,
            x=w_percent(60), y=h_percent(20), width=w_percent(20), height=h_percent(10),

            label_text="Accepter",

            style=texture.Button.Style1
        )

        self.accept.add_listener("on_click_release", lambda *_: self.choose_save(value=True))

    def choose_save(self, value: bool):
        PacketResponseSave(value=value).send_connection(self.game_scene.connection)
        self.window.remove_scene(self)
        self.game_scene.save(value=value)

