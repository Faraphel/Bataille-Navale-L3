import itertools
from math import inf
from typing import TYPE_CHECKING

import pyglet.app

from source.gui import widget, texture, media
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

        # Plein écran

        self.fullscreen = self.add_widget(
            widget.Checkbox,

            x=70*vw, y=87*vh, width=6*vw, height=10*vh,

            style=texture.Checkbox.Style1,

            state=self.window.fullscreen
        )

        self.fullscreen.add_listener(
            "on_state_change",
            lambda widget, *_: self.window.set_fullscreen(widget.state)
        )

        self.add_widget(
            widget.Text,

            x=80*vw, y=90*vh,

            text="Plein écran",
            font_size=20,
        )

        # Vsync

        self.vsync = self.add_widget(
            widget.Checkbox,

            x=70 * vw, y=76 * vh, width=6 * vw, height=10 * vh,

            style=texture.Checkbox.Style1,

            state=self.window.vsync
        )

        self.vsync.add_listener(
            "on_state_change",
            lambda widget, *_: self.window.set_vsync(widget.state)
        )

        self.add_widget(
            widget.Text,

            x=80 * vw, y=79 * vh,

            text="V-Sync",
            font_size=20,
        )

        # Compteur de FPS

        self.show_fps = self.add_widget(
            widget.Checkbox,

            x=70 * vw, y=65 * vh, width=6 * vw, height=10 * vh,

            style=texture.Checkbox.Style1,

            state=self.window.fps_enable
        )

        self.show_fps.add_listener(
            "on_state_change",
            lambda widget, *_: self.window.set_fps_enabled(widget.state)
        )

        self.add_widget(
            widget.Text,

            x=80 * vw, y=68 * vh,

            text="Compteur FPS",
            font_size=20,
        )

        # Limite FPS

        self.fps_limit = self.add_widget(
            widget.Scroller,

            x=70*vw, y=54*vh, width=20*vw, height=10*vh,

            style=texture.Scroller.Style1,
            from_=1,
            value=fps if (fps := self.window.get_fps()) <= 240 else 250,
            to=250,

            text_transform=lambda value: round(value) if value <= 240 else "Illimité"
        )

        self.fps_limit.add_listener(
            "on_value_change",
            lambda widget, *_: self.window.set_fps(widget.value if widget.value <= 240 else inf)
        )

        self.add_widget(
            widget.Text,

            x=92 * vw, y=57 * vh,

            text="FPS",
            font_size=20,
        )

        # Volume

        self.volume_sfx = self.add_widget(
            widget.Scroller,

            x=5 * vw, y=87 * vh, width=20 * vw, height=10 * vh,

            style=texture.Scroller.Style1,
            from_=0,
            value=media.Game.get_volume(),
            to=1,

            text_transform=lambda value: f"{round(value * 100)}%"
        )

        def change_volume_sfx(widget):
            media.Game.set_volume(widget.value)

        self.volume_sfx.add_listener(
            "on_value_change",
            change_volume_sfx
        )

        self.add_widget(
            widget.Text,

            x=27 * vw, y=90 * vh,

            text="Effets Sonore",
            font_size=20,
        )
