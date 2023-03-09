import json
import math
from pathlib import Path
from typing import TYPE_CHECKING

from source.gui.position import vw, vh, top, vh_full, vw_full
from source.path import path_history
from source.gui import widget, texture, media
from source.gui.scene.abc import Scene
from source.utils import path_ctime_str

if TYPE_CHECKING:
    from source.gui.window import Window


class HistoryMenu(Scene):
    PAGE_SIZE: int = 8

    def __init__(self, window: "Window", page: int = 0, **kwargs):
        super().__init__(window, **kwargs)

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=vw_full, height=vh_full,

            image=texture.Background.time
        )

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=20*vw, height=10*vh,

            label_text="Retour",

            style=texture.Button.Style1
        )

        from source.gui.scene import MainMenu
        self.back.add_listener("on_click_release", lambda *_: self.window.set_scene(MainMenu))

        # génère les boutons des sauvegardes
        paths: list[Path] = list(path_history.iterdir())
        page_max: int = math.ceil(len(paths) / self.PAGE_SIZE)

        self.title = self.add_widget(
            widget.Text,

            x=50*vw, y=80*vh,

            anchor_x="center",

            text=f"Page {page+1}/{page_max}",
            font_size=50
        )

        for i, path in enumerate(paths[page*self.PAGE_SIZE:(page+1)*self.PAGE_SIZE]):
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
                title = (
                    f"{data['name_ally']} VS. {data['name_enemy']} "
                    f"({'Gagné' if data['my_turn'] else 'Perdu'}) "
                    f"- {path_ctime_str(path)}"
                )

            button = self.add_widget(
                widget.Button,

                x=25*vw, y=top((25 + (i*9))*vh), width=50*vw, height=8*vh,

                label_text=title,

                style=texture.Button.Style1
            )

            from source.gui.scene import HistoryGame
            button.add_listener(
                "on_click_release",
                (lambda path: (lambda *_: self.window.set_scene(HistoryGame, history_path=path)))(path)
            )

        if page > 0:
            # si nous ne sommes pas à la première page, ajoute un bouton "précédent".
            self.previous = self.add_widget(
                widget.Button,
                x=10*vw, y=45*vh, width=8*vw, height=15*vh,

                label_text="<",
                label_font_size=30,

                style=texture.Button.Style1
            )

            self.previous.add_listener(
                "on_click_release",
                lambda *_: self.window.set_scene(self.__class__, page=page-1)
            )

        if page < page_max - 1:
            # si nous ne sommes pas à la dernière page, ajoute un bouton "suivant".
            self.next = self.add_widget(
                widget.Button,
                x=80*vw, y=45*vh, width=8*vw, height=15*vh,

                label_text=">",
                label_font_size=30,

                style=texture.Button.Style1
            )

            self.next.add_listener(
                "on_click_release",
                lambda *_: self.window.set_scene(self.__class__, page=page+1)
            )

        media.SoundAmbient.menu.play_safe(loop=True)
