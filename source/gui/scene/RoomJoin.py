from typing import TYPE_CHECKING

import pyglet

from source import network
from source.gui.scene.abc import Scene
from source.gui import widget, texture
from source.utils.dict import dict_add_prefix

if TYPE_CHECKING:
    from source.gui.window import Window


class RoomJoin(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1
        )

        from source.gui.scene import MainMenu
        self.back.add_listener("on_click_release", lambda *_: self.window.set_scene(MainMenu))

        self.entry_ip = self.add_widget(
            widget.Input,
            x=0.4, y=0.5, width=0.13, height=0.1,

            regex=r"\d{1,3}(\.\d{1,3}){3}",

            style=texture.Input.Style1
        )

        self.entry_port = self.add_widget(
            widget.Input,
            x=0.53, y=0.5, width=0.07, height=0.1,

            regex=r"\d{0,5}",

            style=texture.Input.Style1
        )

        self.connect = self.add_widget(
            widget.Button,
            x=0.4, y=0.4, width=0.2, height=0.1,

            label_text="Se connecter",

            style=texture.Button.Style1
        )

        self.connect.add_listener("on_click_release", lambda *_: network.Client(
            window=self.window,
            ip_address=self.entry_ip.text,
            daemon=True,
            username="Client"
        ).start())

    def on_draw(self):
        self.back.draw()
        self.entry_ip.draw()
        self.entry_port.draw()
        self.connect.draw()
