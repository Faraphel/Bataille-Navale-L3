from typing import TYPE_CHECKING

import requests

from source import network
from source.gui.scene.abc import Scene
from source.gui import widget, texture
from source.utils.thread import in_pyglet_context, StoppableThread

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.network.packet import PacketSettings


class RoomHost(Scene):
    def __init__(self, window: "Window", port: int, username: str, settings: "PacketSettings", **kwargs):
        super().__init__(window, **kwargs)

        self.username: str = username
        self.ip_address: str = "127.0.0.1"
        self.port: int = port

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1
        )

        self.back.add_listener("on_click_release", self.button_back_callback)

        self.label_ip = self.add_widget(
            widget.Text,

            x=0.5, y=0.55,

            anchor_x="center", anchor_y="center",
            font_size=20
        )

        self.description = self.add_widget(
            widget.Text,

            x=0.5, y=0.45,

            anchor_x="center", anchor_y="center",
            text="En attente d'un second joueur..."
        )

        self.thread_network = network.Host(
            window=self.window,
            daemon=True,
            port=self.port,
            username=self.username,
            settings=settings
        )
        self.thread_network.start()

        self._refresh_ip_text()

        self.thread_ip = StoppableThread(target=self._refresh_ip)  # NOQA
        self.thread_ip.start()

    def _refresh_ip(self):
        while True:
            try:
                response = requests.get('https://api.ipify.org', timeout=10)
                response.raise_for_status()
                break
            except (requests.HTTPError, requests.Timeout):
                if self.thread_ip.stopped: return

        self.ip_address: str = response.content.decode('utf8')

        in_pyglet_context(self._refresh_ip_text)

    def _refresh_ip_text(self):
        self.label_ip.text = f"{self.ip_address}:{self.port}"

    def button_back_callback(self, *_):
        self.thread_network.stop()
        self.thread_ip.stop()
        from source.gui.scene import MainMenu
        self.window.set_scene(MainMenu)
