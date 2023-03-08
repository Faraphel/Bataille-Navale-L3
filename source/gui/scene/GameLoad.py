from pathlib import Path
from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import vw_full, vw, vh, right, px, vw_center, vh_center, vh_full
from source.gui.scene.abc import Scene
from source.network import Host
from source.utils import path_ctime_str

if TYPE_CHECKING:
    from source.gui.window import Window


class GameLoad(Scene):
    def __init__(self, window: "Window", path: Path, thread_host: Host, **kwargs):
        super().__init__(window, **kwargs)

        self.thread_host = thread_host  # thread de l'hôte

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=vw_full, height=vh_full,

            image=texture.Background.choice
        )

        self.label = self.add_widget(
            widget.Text,

            x=vw_center, y=vh_center, width=vw_full,

            anchor_x="center",

            text=f"Une ancienne partie contre cet adversaire a été sauvegardé.\n"
                 f"Souhaitez-vous la reprendre ?\n"
                 f"({path_ctime_str(path)})",
            align="center",
            multiline=True,
            font_size=28,
        )

        self.refuse = self.add_widget(
            widget.Button,

            x=20, y=20, width=20*vw, height=10*vh,

            label_text="Refuser",

            style=texture.Button.Style1
        )

        self.refuse.add_listener("on_click_release", lambda *_: self.response(value=False))

        self.accept = self.add_widget(
            widget.Button,

            x=right(20*px), y=20, width=20*vw, height=10*vh,

            label_text="Accepter",

            style=texture.Button.Style1
        )

        self.accept.add_listener("on_click_release", lambda *_: self.response(value=True))

    def response(self, value: bool):
        self.thread_host.accept_load = value
        self.window.remove_scene(self)

        with self.thread_host.condition_load:
            self.thread_host.condition_load.notify_all()
