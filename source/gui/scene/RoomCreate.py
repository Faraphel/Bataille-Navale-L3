from typing import TYPE_CHECKING

import pyglet

from source.gui import widget, texture
from source.gui.scene import RoomHost
from source.gui.scene.abc import Scene

if TYPE_CHECKING:
    from source.gui.window import Window


class RoomCreate(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.batch_label = pyglet.graphics.Batch()
        self.batch_input_background = pyglet.graphics.Batch()
        self.batch_button_background = pyglet.graphics.Batch()

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

        self.add_widget(
            widget.Text,

            x=0.1, y=0.9,
            anchor_x="center", anchor_y="center",
            text=f"Largeur de la grille",

            batch=self.batch_label
        )

        input_width = self.add_widget(
            widget.Input,

            x=0.2, y=0.86, width=0.1, height=0.08,

            regex=r"\d+",

            style=texture.Input.Style1,

            label_text="8",

            background_batch=self.batch_input_background,
            label_batch=self.batch_label
        )

        self.add_widget(
            widget.Text,

            x=0.1, y=0.8,
            anchor_x="center", anchor_y="center",
            text=f"Longueur de la grille",

            batch=self.batch_label
        )

        input_height = self.add_widget(
            widget.Input,

            x=0.2, y=0.76, width=0.1, height=0.08,

            regex=r"\d+",

            style=texture.Input.Style1,

            label_text="8",

            background_batch=self.batch_input_background,
            label_batch=self.batch_label
        )

        self.start = self.add_widget(
            widget.Button,
            x=lambda widget: widget.scene.window.width - 20 - widget.width, y=20, width=0.2, height=0.1,

            label_text="Continuer",

            style=texture.Button.Style1,

            background_batch=self.batch_button_background,
            label_batch=self.batch_label
        )

        self.start.add_listener("on_click_release", lambda *_: self.window.set_scene(RoomHost))

    def on_draw(self):
        self.batch_input_background.draw()
        self.batch_button_background.draw()
        self.batch_label.draw()
