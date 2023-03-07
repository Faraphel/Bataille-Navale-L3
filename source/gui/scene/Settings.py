from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import vw_full, vh_full, vw, vh
from source.gui.scene.abc.Popup import Popup

if TYPE_CHECKING:
    from source.gui.window import Window


class Settings(Popup):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=vw_full, height=vh_full,

            image=texture.Popup.Style1.background
        )

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=20*vw, height=10*vh,

            label_text="Retour",

            style=texture.Button.Style1
        )

        self.back.add_listener("on_click_release", lambda *_: self.window.remove_scene(self))

        self.checkbox = self.add_widget(
            widget.Checkbox,

            x=45*vw, y=45*vh, width=10*vw, height=10*vh,

            style=texture.Checkbox.Style1
        )

        self.checkbox.add_listener("on_click_release",
                                   lambda *_: self.window.set_fullscreen(self.checkbox.state))

        self.scroller = self.add_widget(
            widget.Scroller,

            x=30*vw, y=20*vh, width=30*vw, height=10*vh,

            style=texture.Scroller.Style1,

            text_transform=lambda value: round(value, 2)
        )
