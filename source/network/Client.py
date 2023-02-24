import socket
from typing import TYPE_CHECKING, Any

from source.gui import scene
from source.network import game_network
from source.network.packet import PacketUsername
from source.network.packet.abc import Packet
from source.utils import StoppableThread
from source.utils.thread import in_pyglet_context

if TYPE_CHECKING:
    from source.gui.window import Window


class Client(StoppableThread):
    """
    The thread executed on the person who join a room.
    """

    def __init__(self, window: "Window", username: str, ip_address: str, port: int = 52321, **kw):
        super().__init__(**kw)

        self.window = window
        self.username = username
        self.ip_address = ip_address
        self.port = port

    def run(self) -> None:
        print("[Client] Thread démarré")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.connect((self.ip_address, self.port))
            connection.settimeout(5)  # défini le timeout à 5 secondes

            print(f"[Client] Connecté avec {connection}")

            settings: Any = Packet.from_connection(connection)
            PacketUsername(username=self.username).send_connection(connection)

            game_scene = in_pyglet_context(
                self.window.set_scene,
                scene.Game,

                connection=connection,

                boats_length=settings.boats_length,
                name_ally=self.username,
                name_enemy=settings.username,
                grid_width=settings.grid_width,
                grid_height=settings.grid_height,
                my_turn=not settings.host_start
            )

            game_network(
                thread=self,
                connection=connection,
                game_scene=game_scene,
            )
