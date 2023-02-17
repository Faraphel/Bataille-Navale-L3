import socket
from threading import Thread
from typing import TYPE_CHECKING

import pyglet.clock

from source.gui import scene


if TYPE_CHECKING:
    from source.gui.window import Window


class Client(Thread):
    def __init__(self, window: "Window", username: str, ip_address: str, port: int = 52321, **kw):
        super().__init__(**kw)

        self.window = window
        self.username = username
        self.ip_address = ip_address
        self.port = port

    def run(self) -> None:
        print("[Client] Thread démarré")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip_address, self.port))

            print(f"[Client] Connecté avec {s}")

            pyglet.clock.schedule_once(lambda dt: self.window.set_scene(scene.Game), 0)

