from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import vw_full, vw_center, vh_center, right, px, vw, vh
from source.gui.scene.abc import Scene


if TYPE_CHECKING:
    from source.gui.window import Window


class GameError(Scene):
    def __init__(self, window: "Window", text: str, **kwargs):
        super().__init__(window, **kwargs)

        self.label = self.add_widget(
            widget.Text,

            x=vw_center, y=vh_center, width=vw_full,

            anchor_x="center",

            text=text,
            align="center",
            multiline=True,
            font_size=28,
        )

        self.back = self.add_widget(
            widget.Button,

            x=right(20*px), y=20, width=20*vw, height=10*vh,

            label_text="Retour",

            style=texture.Button.Style1
        )

        from source.gui.scene import MainMenu
        self.back.add_listener("on_click_release", lambda *_: self.window.set_scene(MainMenu))
