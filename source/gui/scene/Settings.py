from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.scene.abc.Popup import Popup

if TYPE_CHECKING:
    from source.gui.window import Window


class Settings(Popup):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=1.0, height=1.0,

            image=texture.Popup.Style1.background
        )

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1
        )

        self.back.add_listener("on_click_release", lambda *_: self.window.remove_scene(self))

        self.checkbox = self.add_widget(
            widget.Checkbox,

            x=0.45, y=0.45, width=0.1, height=0.1,

            style=texture.Checkbox.Style1
        )

        self.checkbox.add_listener("on_click_release",
                                   lambda *_: self.window.set_fullscreen(self.checkbox.state))

        self.scroller = self.add_widget(
            widget.Scroller,

            x=0.3, y=0.2, width=0.3, height=0.1,

            style=texture.Scroller.Style1,

            text_transform=lambda value: round(value, 2)
        )
