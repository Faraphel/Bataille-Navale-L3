from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.scene.abc import Scene


if TYPE_CHECKING:
    from source.gui.window import Window


class GameError(Scene):
    def __init__(self, window: "Window", text: str, **kwargs):
        super().__init__(window, **kwargs)

        self.label = self.add_widget(
            widget.Text,

            x=0.5, y=0.5, width=1.0,

            anchor_x="center",

            text=text,
            font_size=28,
        )

        self.back = self.add_widget(
            widget.Button,

            x=lambda widget: widget.scene.window.width - 20 - widget.width, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1
        )

        from source.gui.scene import MainMenu
        self.back.add_listener("on_click_release", lambda *_: self.window.set_scene(MainMenu))
