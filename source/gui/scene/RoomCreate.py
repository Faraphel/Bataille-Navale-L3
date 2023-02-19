from typing import TYPE_CHECKING

import pyglet
import requests

from source import network
from source.gui.scene.abc import Scene
from source.gui import widget, texture
from source.utils.dict import dict_add_prefix

if TYPE_CHECKING:
    from source.gui.window import Window


class RoomCreate(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        r = requests.get('https://api.ipify.org')
        r.raise_for_status()
        ip_address: str = r.content.decode('utf8')
        port: int = 52321

        self.batch_button_background = pyglet.graphics.Batch()
        self.batch_label = pyglet.graphics.Batch()

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1,

            background_batch=self.batch_button_background,
            label_batch=self.batch_label
        )

        from source.gui.scene import MainMenu
        self.back.add_listener("on_click_release", lambda *_: self.window.set_scene(MainMenu))

        self.label_ip = self.add_widget(
            widget.Text,

            x=0.5, y=0.55,

            anchor_x="center", anchor_y="center",
            text=f"Votre IP - {ip_address}:{port}",
            font_size=20,

            batch=self.batch_label
        )

        self.description = self.add_widget(
            widget.Text,

            x=0.5, y=0.45,

            anchor_x="center", anchor_y="center",
            text="En attente d'un second joueur...",

            batch=self.batch_label
        )

        self.thread = network.Host(window=self.window, daemon=True, username="Host")
        self.thread.start()

    def on_draw(self):
        self.batch_button_background.draw()
        self.batch_label.draw()
