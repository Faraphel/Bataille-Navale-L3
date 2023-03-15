from typing import TYPE_CHECKING

from source.gui.position import vw_full, vh_full, vw, vh
from source.gui.scene.abc import Scene
from source.gui import widget, scene, texture, media

if TYPE_CHECKING:
    from source.gui.window import Window


class MainMenu(Scene):
    """
    Cette scène représente le menu principal
    """

    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=vw_full, height=vh_full,

            image=texture.Background.main
        )

        self.title = self.add_widget(
            widget.Text,

            x=50, y=85*vh,

            text="Bataille Navale",
            font_size=50
        )

        self.game_create = self.add_widget(
            widget.Button,
            x=50, y=50*vh, width=30*vw, height=10*vh,

            label_text="Créer une salle",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.game_create.add_listener("on_click_release", lambda *_: self.window.set_scene(scene.RoomCreate))

        self.game_join = self.add_widget(
            widget.Button,

            x=50, y=35*vh, width=30*vw, height=10*vh,

            label_text="Rejoindre une salle",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.game_join.add_listener("on_click_release", lambda *_: self.window.set_scene(scene.RoomJoin))

        self.history = self.add_widget(
            widget.Button,

            x=50, y=20*vh, width=30*vw, height=10*vh,

            label_text="Historique",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.history.add_listener("on_click_release", lambda *_: self.window.set_scene(scene.HistoryMenu))

        self.settings = self.add_widget(
            widget.Button,

            x=50, y=5*vh, width=30*vw, height=10*vh,

            label_text="Paramètres",
            label_font_size=20,

            style=texture.Button.Style1
        )

        self.settings.add_listener("on_click_release", lambda *_: self.window.add_scene(scene.Settings))

        media.SoundAmbient.menu.play_safe(loop=True)
