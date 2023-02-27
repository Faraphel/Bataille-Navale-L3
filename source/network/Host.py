import socket
from typing import TYPE_CHECKING, Any

from source.gui import scene
from source.network import game_network
from source.network.packet.abc import Packet
from source.utils import StoppableThread
from source.utils.thread import in_pyglet_context

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.network.packet import PacketSettings


class Host(StoppableThread):
    """
    The thread executed on the person who create a room.
    """

    def __init__(self, window: "Window", port: int, settings: "PacketSettings", **kw):
        super().__init__(**kw)

        self.window = window
        self.settings = settings
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
                    if self.stopped: return  # vérifie si le thread n'est pas censé s'arrêter
                    # sinon, réessaye

            print(f"[Serveur] Connecté avec {address}")

            self.settings.send_connection(connection)
            packet_username: Any = Packet.from_connection(connection)

            game_scene = in_pyglet_context(
                self.window.set_scene,
                scene.Game,

                connection=connection,

                boats_length=self.settings.boats_length,
                name_ally=self.settings.username,
                name_enemy=packet_username.username,
                grid_width=self.settings.grid_width,
                grid_height=self.settings.grid_height,
                my_turn=self.settings.host_start
            )

            game_network(
                thread=self,
                connection=connection,
                game_scene=game_scene
            )
