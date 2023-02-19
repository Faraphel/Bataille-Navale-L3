from typing import TYPE_CHECKING

from source.gui.scene.abc import Scene
from source.gui import widget, scene, texture
from source.utils.dict import dict_add_prefix

if TYPE_CHECKING:
    from source.gui.window import Window


class MainMenu(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        self.background = self.add_widget(
            widget.Image,
            x=0.0, y=0.0, width=1.0, height=1.0,
            image=texture.Background.main
        )

        self.title = self.add_widget(
            widget.Text,
            x=50, y=0.85,
            text="Bataille Navale",
            font_size=50
        )

        self.game_create = self.add_widget(
            widget.Button,

            x=50, y=0.45, width=0.3, height=0.1,

            label_text="Créer une salle",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.game_create.add_listener("on_click_release", lambda *_: self.window.set_scene(scene.RoomCreate))

        self.game_join = self.add_widget(
            widget.Button,

            x=50, y=0.3, width=0.3, height=0.1,

            label_text="Rejoindre une salle",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.game_join.add_listener("on_click_release", lambda *_: self.window.set_scene(scene.RoomJoin))

        self.settings = self.add_widget(
            widget.Button,

            x=50, y=0.15, width=0.3, height=0.1,

            label_text="Paramètres",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.settings.add_listener("on_click_release", lambda *_: self.window.set_scene(scene.Settings))

    def on_draw(self):
        self.background.draw()
        self.title.draw()
        self.game_create.draw()
        self.game_join.draw()
        self.settings.draw()
