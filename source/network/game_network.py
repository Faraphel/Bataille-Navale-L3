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


def game_network(thread: "StoppableThread", window: "Window", connection: socket.socket, host: bool):
    """
    Run the networking to make the game work and react with the other player
    :param thread: the thread where this function is called.
    :param window: the window of the game
    :param connection: the connection with the other player
    """

    game_scene = in_pyglet_context(window.set_scene, scene.Game, connection=connection)
    game_scene.my_turn = host

    while True:
        data: Any = Packet.from_connection(connection)

        if data is None:
            if thread.stopped: return  # vérifie si le thread n'est pas censé s'arrêter
            continue

        match type(data):
            case packet.PacketChat:
                print(data.message)

            case packet.PacketBoatPlaced:
                game_scene.boat_ready_enemy = True
                print("adversaire à posé ses bateaux")

            case packet.PacketBombPlaced:
                try:
                    bomb_state = game_scene.grid_ally.board.bomb(data.position)
                except (InvalidBombPosition, PositionAlreadyShot):
                    bomb_state = BombState.ERROR

                packet.PacketBombState(position=data.position, bomb_state=bomb_state).send_connection(connection)

                touched = bomb_state in [BombState.TOUCHED, BombState.SUNKEN, BombState.WON]

                if touched:
                    in_pyglet_context(game_scene.boat_broken_enemy)

                game_scene.my_turn = not (touched or (bomb_state is BombState.ERROR))

            case packet.PacketBombState:
                print(data.bomb_state)
                if data.bomb_state is BombState.ERROR:
                    game_scene.my_turn = True
                    continue

                touched = data.bomb_state in [BombState.TOUCHED, BombState.SUNKEN, BombState.WON]
                game_scene.my_turn = touched

                if touched:
                    in_pyglet_context(game_scene.boat_broken_ally)

                in_pyglet_context(game_scene.grid_enemy.place_bomb, data.position, touched)
