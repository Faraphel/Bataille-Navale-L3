from typing import TYPE_CHECKING

from source.gui.event import StopEvent
from source.gui.scene.abc import Scene
from source.gui import widget, texture

if TYPE_CHECKING:
    from source.gui.window import Window


class Settings(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

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

    def on_mouse_press_after(self, x: int, y: int, button: int, modifiers: int):
        raise StopEvent()

    def on_mouse_motion_after(self, x: int, y: int, button: int, modifiers: int):
        raise StopEvent()
