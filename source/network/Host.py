import socket
from threading import Thread
from typing import TYPE_CHECKING

import pyglet

from source.gui import scene


if TYPE_CHECKING:
    from source.gui.window import Window


class Host(Thread):
    def __init__(self, window: "Window", username: str, port: int = 52321, **kw):
        super().__init__(**kw)

        self.window = window
        self.username = username
        self.port = port

    def run(self) -> None:
        print("[Serveur] Thread démarré")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", self.port))
            s.listen()
            connection, address = s.accept()

            print(f"[Serveur] Connecté avec {address}")

            pyglet.clock.schedule_once(lambda dt: self.window.set_scene(scene.Game), 0)


