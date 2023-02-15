from typing import TYPE_CHECKING

import pyglet

from source.gui.scene import RoomJoin, RoomCreate, Settings
from source.gui.scene.abc import Scene
from source.gui.widget import Image, Text, Button, FPSDisplay

if TYPE_CHECKING:
    from source.gui.window import Window


class MainMenu(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        texture_background = pyglet.image.load("./assets/image/background/main.jpeg")
        texture_button_normal = pyglet.image.load("./assets/image/button/normal.png")
        texture_button_hover = pyglet.image.load("./assets/image/button/hovering.png")
        texture_button_click = pyglet.image.load("./assets/image/button/clicking.png")

        self.background = self.add_widget(
            Image,
            x=0.0, y=0.0, width=1.0, height=1.0,
            image=texture_background
        )

        self.title = self.add_widget(
            Text,
            x=50, y=0.85,
            text="Bataille Navale",
            font_size=50
        )

        self.game_create = self.add_widget(
            Button,

            x=50, y=0.45, width=0.3, height=0.1,

            label_text="Créer une salle",
            label_font_size=20,

            texture_normal=texture_button_normal,
            texture_hover=texture_button_hover,
            texture_click=texture_button_click
        )

        self.game_create.on_release = lambda button, modifiers: self.window.set_scene(RoomCreate)

        self.game_join = self.add_widget(
            Button,

            x=50, y=0.3, width=0.3, height=0.1,

            label_text="Rejoindre une salle",
            label_font_size=20,

            texture_normal=texture_button_normal,
            texture_hover=texture_button_hover,
            texture_click=texture_button_click
        )

        self.game_join.on_release = lambda button, modifiers: self.window.set_scene(RoomJoin)

        self.settings = self.add_widget(
            Button,

            x=50, y=0.15, width=0.3, height=0.1,

            label_text="Paramètres",
            label_font_size=20,

            texture_normal=texture_button_normal,
            texture_hover=texture_button_hover,
            texture_click=texture_button_click
        )

        self.settings.on_release = lambda button, modifiers: self.window.set_scene(Settings)

        self.fps_display = self.add_widget(FPSDisplay, color=(255, 255, 255, 180))

    def on_draw(self):
        self.background.draw()
        self.title.draw()
        self.game_create.draw()
        self.game_join.draw()
        self.settings.draw()

        self.fps_display.draw()
