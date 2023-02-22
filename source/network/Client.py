import socket
from queue import Queue
from typing import TYPE_CHECKING

import pyglet.clock

from source.core.enums import BombState
from source.core.error import PositionAlreadyShot, InvalidBombPosition
from source.gui import scene
from source.network.SocketType import SocketType
from source.network.packet.Bomb import Bomb
from source.network.packet.PacketBombState import PacketBombState
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

            def create_game_scene(dt: float, queue: Queue):
                game_scene = self.window.set_scene(scene.Game, connection=connection)
                queue.put(game_scene)

            queue = Queue()
            pyglet.clock.schedule_once(create_game_scene, 0, queue)
            game_scene = queue.get()

            while True:
                data = None

                try: data = connection.recv(1)
                except socket.timeout: pass

                if not data:
                    if self._stop: return  # vérifie si le thread n'est pas censé s'arrêter
                    continue

                socket_type = SocketType(int.from_bytes(data, "big"))

                match socket_type:
                    case SocketType.CHAT: print(connection.recv(1024).decode())
                    case SocketType.BOAT_PLACED: print("adversaire à posé ses bateaux")
                    case SocketType.BOMB:
                        bomb = Bomb.from_bytes(connection.recv(2))

                        try: bomb_state = game_scene.grid_ally.board.bomb((bomb.x, bomb.y))
                        except (InvalidBombPosition, PositionAlreadyShot): pass  # TODO: gérer les erreurs

                        connection.send(SocketType.BOMB_STATE.value.to_bytes(1, "big"))

                        packet_bomb_state = PacketBombState(
                            x=bomb.x,
                            y=bomb.y,
                            bomb_state=bomb_state
                        )
                        connection.send(packet_bomb_state.to_bytes())

                    case SocketType.BOMB_STATE:
                        packet_bomb_state = PacketBombState.from_bytes(connection.recv(3))

                        touched = packet_bomb_state.bomb_state in [BombState.TOUCHED, BombState.SUNKEN, BombState.WON]

                        pyglet.clock.schedule_once(
                            lambda dt: game_scene.grid_enemy.place_bomb((packet_bomb_state.x, packet_bomb_state.y),
                                                                             touched),
                            0
                        )
