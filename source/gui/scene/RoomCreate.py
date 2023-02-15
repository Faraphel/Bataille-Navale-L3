from typing import TYPE_CHECKING

import pyglet
import requests

from source.gui.scene.abc import Scene
from source.gui.widget import Text, Button

if TYPE_CHECKING:
    from source.gui.window import Window


class RoomCreate(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        r = requests.get('https://api.ipify.org')
        r.raise_for_status()
        ip_address: str = r.content.decode('utf8')
        port: str = "6464"

        texture_button_normal = pyglet.image.load("./assets/image/button/normal.png")
        texture_button_hover = pyglet.image.load("./assets/image/button/hovering.png")
        texture_button_click = pyglet.image.load("./assets/image/button/clicking.png")

        self.back = self.add_widget(
            Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            texture_normal=texture_button_normal,
            texture_hover=texture_button_hover,
            texture_click=texture_button_click
        )

        from source.gui.scene import MainMenu
        self.back.on_release = lambda button, modifiers: self.window.set_scene(MainMenu)

        self.label_ip = self.add_widget(
            Text,
            x=0.5, y=0.55,
            anchor_x="center", anchor_y="center",
            text=f"Votre IP - {ip_address}:{port}",
            font_size=20
        )

        self.description = self.add_widget(
            Text,
            x=0.5, y=0.45,
            anchor_x="center", anchor_y="center",
            text="En attente d'un second joueur..."
        )

    def on_draw(self):
        self.back.draw()
        self.label_ip.draw()
        self.description.draw()
