from typing import TYPE_CHECKING

from source.gui.scene.abc import Scene
from source.gui import widget, texture
from source.utils.dict import dict_add_prefix

if TYPE_CHECKING:
    from source.gui.window import Window


class Settings(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1
        )

        from source.gui.scene import MainMenu
        self.back.add_listener("on_click_release", lambda *_: self.window.set_scene(MainMenu))

        self.checkbox = self.add_widget(
            widget.Checkbox,

            x=0.45, y=0.45, width=0.1, height=0.1,

            style=texture.Checkbox.Style1
        )

        self.scroller = self.add_widget(
            widget.Scroller,

            x=0.3, y=0.2, width=0.3, height=0.1,

            style=texture.Scroller.Style1,

            text_transform=lambda value: round(value, 2),
        )

    def on_draw(self):
        self.checkbox.draw()
        self.scroller.draw()
        self.back.draw()
