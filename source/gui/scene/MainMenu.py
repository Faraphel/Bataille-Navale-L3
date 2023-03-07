from typing import TYPE_CHECKING

from source.gui.position import w_full, h_full, h_percent, w_percent
from source.gui.scene.abc import Scene
from source.gui import widget, scene, texture

if TYPE_CHECKING:
    from source.gui.window import Window


class MainMenu(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=w_full, height=h_full,

            image=texture.Background.main
        )

        self.title = self.add_widget(
            widget.Text,

            x=50, y=h_percent(85),

            text="Bataille Navale",
            font_size=50
        )

        self.game_create = self.add_widget(
            widget.Button,
            x=50, y=h_percent(50), width=w_percent(30), height=h_percent(10),

            label_text="Créer une salle",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.game_create.add_listener("on_click_release", lambda *_: self.window.set_scene(scene.RoomCreate))

        self.game_join = self.add_widget(
            widget.Button,

            x=50, y=h_percent(35), width=w_percent(30), height=h_percent(10),

            label_text="Rejoindre une salle",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.game_join.add_listener("on_click_release", lambda *_: self.window.set_scene(scene.RoomJoin))

        self.history = self.add_widget(
            widget.Button,

            x=50, y=h_percent(20), width=w_percent(30), height=h_percent(10),

            label_text="Historique",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.history.add_listener("on_click_release", lambda *_: self.window.set_scene(scene.HistoryMenu))

        self.settings = self.add_widget(
            widget.Button,

            x=50, y=h_percent(5), width=w_percent(30), height=h_percent(10),

            label_text="Paramètres",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.settings.add_listener("on_click_release", lambda *_: self.window.add_scene(scene.Settings))
