import math
from pathlib import Path
from typing import TYPE_CHECKING

from source.path import path_history
from source.gui import widget, texture
from source.gui.scene.abc import Scene


if TYPE_CHECKING:
    from source.gui.window import Window


class HistoryMenu(Scene):
    PAGE_SIZE: int = 8

    def __init__(self, window: "Window", page: int = 0, **kwargs):
        super().__init__(window, **kwargs)

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

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

            x=0.5, y=0.80,

            anchor_x="center",

            text=f"Page {page+1}/{page_max}",
            font_size=50
        )

        for i, path in enumerate(paths[page*self.PAGE_SIZE:(page+1)*self.PAGE_SIZE]):
            button = self.add_widget(
                widget.Button,

                x=0.25, y=0.75 - ((i+1) * 0.09), width=0.5, height=0.08,

                label_text=path.stem,

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
                x=0.1, y=0.45, width=0.1, height=0.1,

                label_text="Précédent",

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
                x=0.80, y=0.45, width=0.1, height=0.1,

                label_text="Suivant",

                style=texture.Button.Style1
            )

            self.next.add_listener(
                "on_click_release",
                lambda *_: self.window.set_scene(self.__class__, page=page+1)
            )
