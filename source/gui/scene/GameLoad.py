from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.scene.abc import Scene


if TYPE_CHECKING:
    from source.gui.window import Window


class GameLoad(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.label = self.add_widget(
            widget.Text,

            x=0.5, y=0.5, width=1.0,

            anchor_x="center",

            text="Une ancienne partie contre cet adversaire a été sauvegardé.\nSouhaitez-vous la reprendre ?",
            align="center",
            multiline=True,
            font_size=28,
        )

        self.refuse = self.add_widget(
            widget.Button,

            x=20, y=20, width=0.2, height=0.1,

            label_text="Refuser",

            style=texture.Button.Style1
        )

        self.accept = self.add_widget(
            widget.Button,

            x=lambda widget: widget.scene.window.width - 20 - widget.width, y=20, width=0.2, height=0.1,

            label_text="Accepter",

            style=texture.Button.Style1
        )

