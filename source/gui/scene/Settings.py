from typing import TYPE_CHECKING

import pyglet

from source.gui.scene.abc import Scene
from source.gui import widget

if TYPE_CHECKING:
    from source.gui.window import Window


class Settings(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        texture_tick_disabled = pyglet.image.load("./assets/image/checkbox/disabled.png")
        texture_tick_enabled = pyglet.image.load("./assets/image/checkbox/enabled.png")

        texture_scroller_background = pyglet.image.load("./assets/image/scroller/background.png")
        texture_scroller_cursor = pyglet.image.load("./assets/image/scroller/cursor.png")

        texture_button_normal = pyglet.image.load("./assets/image/button/normal.png")
        texture_button_hover = pyglet.image.load("./assets/image/button/hovering.png")
        texture_button_click = pyglet.image.load("./assets/image/button/clicking.png")

        texture_grid_background = pyglet.image.load("./assets/image/grid/background.png")

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            texture_normal=texture_button_normal,
            texture_hover=texture_button_hover,
            texture_click=texture_button_click
        )

        from source.gui.scene import MainMenu
        self.back.on_release = lambda *_: self.window.set_scene(MainMenu)

        self.checkbox = self.add_widget(
            widget.Checkbox,

            x=0.45, y=0.45, width=0.1, height=0.1,

            texture_disabled=texture_tick_disabled,
            texture_enabled=texture_tick_enabled,
        )

        self.scroller = self.add_widget(
            widget.Scroller,

            x=0.3, y=0.2, width=0.3, height=0.1,

            texture_background=texture_scroller_background,
            texture_cursor=texture_scroller_cursor,

            text_transform=lambda value: round(value, 2),
        )

    def on_draw(self):
        self.checkbox.draw()
        self.scroller.draw()
        self.back.draw()
