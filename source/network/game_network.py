import socket
from typing import Any

from source.core.enums import BombState
from source.core.error import InvalidBombPosition, PositionAlreadyShot
from source.gui import scene
from source.network.packet.abc import Packet
from source.network import packet

from source.gui.window import Window
from source.utils import StoppableThread
from source.utils.thread import in_pyglet_context


def game_network(thread: "StoppableThread", window: "Window", connection: socket.socket):
    game_scene = in_pyglet_context(window.set_scene, scene.Game, connection=connection)

    while True:
        data: Any = Packet.from_connection(connection)

        if data is None:
            if thread.stopped: return  # vérifie si le thread n'est pas censé s'arrêter
            continue

        match type(data):
            case packet.PacketChat:
                print(data.message)

            case packet.PacketBoatPlaced:
                print("adversaire à posé ses bateaux")

            case packet.PacketBombPlaced:
                try:
                    bomb_state = game_scene.grid_ally.board.bomb(data.position)
                except (InvalidBombPosition, PositionAlreadyShot):
                    bomb_state = BombState.ERROR

                packet.PacketBombState(position=data.position, bomb_state=bomb_state).send_connection(connection)

            case packet.PacketBombState:
                if data.bomb_state is BombState.ERROR: continue

                touched = data.bomb_state in [BombState.TOUCHED, BombState.SUNKEN, BombState.WON]

                in_pyglet_context(game_scene.grid_enemy.place_bomb, data.position, touched)
