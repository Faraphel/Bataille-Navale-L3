import socket
from typing import Type, Callable

from source.gui.scene import Game
from source.network.packet.abc import Packet
from source.network import packet

from source.utils import StoppableThread
from source.utils.thread import in_pyglet_context


def game_network(
        thread: "StoppableThread",
        connection: socket.socket,
        game_scene: Game,
):
    """
    Run the networking to make the game work and react with the other player
    :param game_scene: the scene of the game
    :param thread: the thread where this function is called.
    :param connection: the connection with the other player
    """

    game_methods: dict[Type["Packet"], Callable] = {
        packet.PacketChat: game_scene.network_on_chat,
        packet.PacketBoatPlaced: game_scene.network_on_boat_placed,
        packet.PacketBombPlaced: game_scene.network_on_bomb_placed,
        packet.PacketBombState: game_scene.network_on_bomb_state,
        packet.PacketQuit: game_scene.network_on_quit,
    }

    while True:
        data_type: Type["Packet"] = Packet.type_from_connection(connection)

        if data_type is None:
            if thread.stopped: return  # vérifie si le thread n'est pas censé s'arrêter
            continue

        data = data_type.from_connection(connection)

        if in_pyglet_context(
            game_methods[data_type], data  # récupère la methode relié ce type de donnée
        ): return  # Appelle la méthode. Si elle renvoie True, arrête le thread
