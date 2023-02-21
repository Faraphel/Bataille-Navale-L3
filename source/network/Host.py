import socket
from typing import TYPE_CHECKING

import pyglet

from source.gui import scene
from source.network.SocketType import SocketType
from source.utils import StoppableThread

if TYPE_CHECKING:
    from source.gui.window import Window


class Host(StoppableThread):
    def __init__(self, window: "Window", username: str, port: int = 52321, **kw):
        super().__init__(**kw)

        self.window = window
        self.username = username
        self.port = port

    def run(self) -> None:
        print("[Serveur] Thread démarré")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("", self.port))  # connecte le socket au port indiqué

            server.settimeout(5)  # défini le timeout à 5 secondes
            server.listen()  # écoute de nouvelle connexion

            while True:
                try:
                    connection, address = server.accept()  # accepte la première connexion entrante
                    break  # sort de la boucle
                except socket.timeout:  # en cas de timeout
                    if self._stop: return  # vérifie si le thread n'est pas censé s'arrêter
                    # sinon, réessaye

            print(f"[Serveur] Connecté avec {address}")

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
