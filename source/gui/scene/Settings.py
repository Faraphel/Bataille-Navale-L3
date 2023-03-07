from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import w_full, h_full, w_percent, h_percent
from source.gui.scene.abc.Popup import Popup

if TYPE_CHECKING:
    from source.gui.window import Window


class Settings(Popup):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=w_full, height=h_full,

            image=texture.Popup.Style1.background
        )

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=w_percent(20), height=h_percent(10),

            label_text="Retour",

            style=texture.Button.Style1
        )

        self.back.add_listener("on_click_release", lambda *_: self.window.remove_scene(self))

        self.checkbox = self.add_widget(
            widget.Checkbox,

            x=w_percent(45), y=h_percent(45), width=w_percent(10), height=h_percent(10),

            style=texture.Checkbox.Style1
        )

        self.checkbox.add_listener("on_click_release",
                                   lambda *_: self.window.set_fullscreen(self.checkbox.state))

        self.scroller = self.add_widget(
            widget.Scroller,

            x=w_percent(30), y=h_percent(20), width=w_percent(30), height=h_percent(10),

            style=texture.Scroller.Style1,

            text_transform=lambda value: round(value, 2)
        )
