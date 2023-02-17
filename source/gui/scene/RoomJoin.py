from typing import TYPE_CHECKING

import pyglet

from source import network
from source.gui.scene.abc import Scene
from source.gui.widget import Input, Button

if TYPE_CHECKING:
    from source.gui.window import Window


class RoomJoin(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        texture_button_normal = pyglet.image.load("./assets/image/button/normal.png")
        texture_button_hover = pyglet.image.load("./assets/image/button/hovering.png")
        texture_button_click = pyglet.image.load("./assets/image/button/clicking.png")

        texture_input_normal = pyglet.image.load("assets/image/input/normal.png")
        texture_input_active = pyglet.image.load("./assets/image/input/active.png")
        texture_input_error = pyglet.image.load("./assets/image/input/error.png")

        self.back = self.add_widget(
            Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            texture_normal=texture_button_normal,
            texture_hover=texture_button_hover,
            texture_click=texture_button_click
        )

        from source.gui.scene import MainMenu
        self.back.on_release = lambda *_: self.window.set_scene(MainMenu)

        self.entry_ip = self.add_widget(
            Input,
            x=0.4, y=0.5, width=0.13, height=0.1,

            regex=r"\d{1,3}(\.\d{1,3}){3}",

            texture_normal=texture_input_normal,
            texture_active=texture_input_active,
            texture_error=texture_input_error
        )

        self.entry_port = self.add_widget(
            Input,
            x=0.53, y=0.5, width=0.07, height=0.1,

            regex=r"\d{0,5}",

            texture_normal=texture_input_normal,
            texture_active=texture_input_active,
            texture_error=texture_input_error
        )

        self.connect = self.add_widget(
            Button,
            x=0.4, y=0.4, width=0.2, height=0.1,

            label_text="Se connecter",

            texture_normal=texture_button_normal,
            texture_hover=texture_button_hover,
            texture_click=texture_button_click
        )

        self.connect.on_release = lambda *_: network.Client(
            window=self.window,
            ip_address=self.entry_ip.text,
            daemon=True
        ).start()

    def on_draw(self):
        self.back.draw()
        self.entry_ip.draw()
        self.entry_port.draw()
        self.connect.draw()
