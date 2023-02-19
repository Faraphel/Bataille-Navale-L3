from typing import TYPE_CHECKING

import pyglet

from source.event.signal import StopEventScene
from source.gui.scene.abc import Scene
from source.gui import widget, texture

if TYPE_CHECKING:
    from source.gui.window import Window


class Settings(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        self.batch_button_background = pyglet.graphics.Batch()
        self.batch_scroller_background = pyglet.graphics.Batch()
        self.batch_scroller_cursor = pyglet.graphics.Batch()
        self.batch_checkbox = pyglet.graphics.Batch()
        self.batch_label = pyglet.graphics.Batch()

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1,

            background_batch=self.batch_button_background,
            label_batch=self.batch_label
        )

        self.back.add_listener("on_click_release", lambda *_: self.window.remove_scene(self))

        self.checkbox = self.add_widget(
            widget.Checkbox,

            x=0.45, y=0.45, width=0.1, height=0.1,

            style=texture.Checkbox.Style1,

            batch=self.batch_checkbox
        )

        self.scroller = self.add_widget(
            widget.Scroller,

            x=0.3, y=0.2, width=0.3, height=0.1,

            style=texture.Scroller.Style1,

            text_transform=lambda value: round(value, 2),

            background_batch=self.batch_scroller_background,
            cursor_batch=self.batch_scroller_cursor,
            label_batch=self.batch_label
        )

    def on_draw(self):
        self.batch_button_background.draw()

        self.batch_scroller_background.draw()
        self.batch_scroller_cursor.draw()

        self.batch_checkbox.draw()

        self.batch_label.draw()

    def on_mouse_press_after(self, x: int, y: int, button: int, modifiers: int):
        raise StopEventScene()

    def on_mouse_motion_after(self, x: int, y: int, button: int, modifiers: int):
        raise StopEventScene()
