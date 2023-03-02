from typing import TYPE_CHECKING

from source import network
from source.gui.scene.abc import Scene
from source.gui import widget, texture

if TYPE_CHECKING:
    from source.gui.window import Window


class RoomJoin(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1
        )

        self.back.add_listener("on_click_release", self.button_back_callback)

        # Pseudo

        self.entry_username = self.add_widget(
            widget.Input,
            x=0.4, y=0.55, width=0.2, height=0.1,

            style=texture.Input.Style1,

            label_text="Client"
        )

        # IP / Port

        self.entry_ip = self.add_widget(
            widget.Input,
            x=0.4, y=0.45, width=0.13, height=0.1,

            regex=r"\d{1,3}(\.\d{1,3}){3}",

            style=texture.Input.Style1,

            label_text="127.0.0.1"
        )

        self.entry_port = self.add_widget(
            widget.Input,
            x=0.53, y=0.45, width=0.07, height=0.1,

            regex=r"\d{1,5}",

            label_text="52321",

            style=texture.Input.Style1
        )

        self.connect = self.add_widget(
            widget.Button,
            x=0.4, y=0.35, width=0.2, height=0.1,

            label_text="Se connecter",

            style=texture.Button.Style1
        )

        self.connect.add_listener("on_click_release", self.button_connect)

    def button_connect(self, widget, *_):
        network.Client(
            window=self.window,
            ip_address=self.entry_ip.text,
            port=int(self.entry_port.text),
            daemon=True,
            username=self.entry_username.text
        ).start()

    def button_back_callback(self, widget, *_):
        from source.gui.scene import MainMenu
        self.window.set_scene(MainMenu)
