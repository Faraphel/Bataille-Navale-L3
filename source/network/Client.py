import socket
from threading import Thread

from source.gui.scene import Game


class Client(Thread):
    def __init__(self, window: "Window", ip_address: str, port: int = 52321, **kw):
        super().__init__(**kw)

        self.window = window
        self.ip_address = ip_address
        self.port = port

    def run(self) -> None:
        print("[Client] Thread démarré")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip_address, self.port))

            print(f"[Client] Connecté avec {s}")

            self.window.set_scene(Game)
