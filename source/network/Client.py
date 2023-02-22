import socket
from typing import TYPE_CHECKING

from source.network import game_network
from source.utils import StoppableThread

if TYPE_CHECKING:
    from source.gui.window import Window


class Client(StoppableThread):
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

            game_network(self, self.window, connection)
