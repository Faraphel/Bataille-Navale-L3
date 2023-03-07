from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import w_full, h_percent, w_percent, right_content
from source.gui.scene.abc import Scene


if TYPE_CHECKING:
    from source.gui.window import Window


class GameError(Scene):
    def __init__(self, window: "Window", text: str, **kwargs):
        super().__init__(window, **kwargs)

        self.label = self.add_widget(
            widget.Text,

            x=w_percent(50), y=h_percent(50), width=w_full,

            anchor_x="center",

            text=text,
            align="center",
            multiline=True,
            font_size=28,
        )

        self.back = self.add_widget(
            widget.Button,

            x=right_content(20), y=20, width=w_percent(20), height=h_percent(10),

            label_text="Retour",

            style=texture.Button.Style1
        )

        from source.gui.scene import MainMenu
        self.back.add_listener("on_click_release", lambda *_: self.window.set_scene(MainMenu))
