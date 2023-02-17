import socket
from threading import Thread

from source.gui.scene import Game


class Host(Thread):
    def __init__(self, window: "Window", port: int = 52321, **kw):
        super().__init__(**kw)

        self.window = window
        self.port = port

    def run(self) -> None:
        print("[Serveur] Thread démarré")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", self.port))
            s.listen()
            connection, address = s.accept()

            print(f"[Serveur] Connecté avec {address}")

            self.window.set_scene(Game)
