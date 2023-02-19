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

        self._stop = False

        self.window = window
        self.username = username
        self.port = port

    def stop(self) -> None:
        self._stop = True

    def run(self) -> None:
        print("[Serveur] Thread démarré")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", self.port))  # connecte le socket au port indiqué

            s.settimeout(5)  # defini le timeout à 5 secondes
            s.listen()  # écoute de nouvelle connexion

            while True:
                try:
                    connection, address = s.accept()  # accepte la première connexion entrante
                    break  # sort de la boucle
                except socket.timeout:  # en cas de timeout
                    if self._stop: return  # vérifie si le thread n'est pas censé s'arrêter
                    # sinon, réessaye

            print(f"[Serveur] Connecté avec {address}")

            pyglet.clock.schedule_once(lambda dt: self.window.set_scene(scene.Game), 0)
