import socket
from threading import Thread
from typing import TYPE_CHECKING

import pyglet.clock

from source.gui import scene
from source.network.SocketType import SocketType

if TYPE_CHECKING:
    from source.gui.window import Window


class Client(Thread):
    def __init__(self, window: "Window", username: str, ip_address: str, port: int = 52321, **kw):
        super().__init__(**kw)

        self._stop = False

        self.window = window
        self.username = username
        self.ip_address = ip_address
        self.port = port

    def stop(self):
        self._stop = True

    def run(self) -> None:
        print("[Client] Thread démarré")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.connect((self.ip_address, self.port))
            connection.settimeout(5)  # défini le timeout à 5 secondes

            print(f"[Client] Connecté avec {connection}")

            pyglet.clock.schedule_once(lambda dt: self.window.set_scene(scene.Game, connection=connection), 0)

            while True:
                data = None

                try: data = connection.recv(1)
                except socket.timeout: pass

                if not data:
                    if self._stop: return  # vérifie si le thread n'est pas censé s'arrêter
                    continue

                socket_type = SocketType(int.from_bytes(data, "big"))

                print(socket_type)

                match socket_type:
                    case SocketType.CHAT: print(connection.recv(1024).decode())
