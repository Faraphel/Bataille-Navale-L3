from typing import TYPE_CHECKING

import pyglet

from source import network
from source.gui.scene.abc import Scene
from source.gui import widget, texture

if TYPE_CHECKING:
    from source.gui.window import Window


class RoomJoin(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.batch_button_background = pyglet.graphics.Batch()
        self.batch_input_background = pyglet.graphics.Batch()
        self.batch_label = pyglet.graphics.Batch()

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1,

            background_batch=self.batch_button_background,
            label_batch=self.batch_label
        )

        self.back.add_listener("on_click_release", self.button_back_callback)

        self.entry_ip = self.add_widget(
            widget.Input,
            x=0.4, y=0.5, width=0.13, height=0.1,

            regex=r"\d{1,3}(\.\d{1,3}){3}",

            style=texture.Input.Style1,

            label_text="127.0.0.1",

            background_batch=self.batch_input_background,
            label_batch=self.batch_label
        )

        self.entry_port = self.add_widget(
            widget.Input,
            x=0.53, y=0.5, width=0.07, height=0.1,

            regex=r"\d{0,5}",

            style=texture.Input.Style1,

            background_batch=self.batch_input_background,
            label_batch=self.batch_label
        )

        self.connect = self.add_widget(
            widget.Button,
            x=0.4, y=0.4, width=0.2, height=0.1,

            label_text="Se connecter",

            style=texture.Button.Style1,

            background_batch=self.batch_button_background,
            label_batch=self.batch_label
        )

        self.connect.add_listener("on_click_release", self.button_connect)

    def button_connect(self, widget, *_):
        network.Client(
            window=self.window,
            ip_address=self.entry_ip.text,
            daemon=True,
            username="Client"
        ).start()

    def button_back_callback(self, widget, *_):
        from source.gui.scene import MainMenu
        self.window.set_scene(MainMenu)

    def on_draw(self):
        self.batch_button_background.draw()
        self.batch_input_background.draw()
        self.batch_label.draw()
