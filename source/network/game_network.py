import socket
from typing import Type, Callable, TYPE_CHECKING

from source.network.packet.abc import Packet
from source.network import packet

from source.utils import StoppableThread
from source.utils.thread import in_pyglet_context


if TYPE_CHECKING:
    from source.gui.scene import Game


def game_network(
        thread: "StoppableThread",
        connection: socket.socket,
        game_scene: "Game",
):
    """
    Partie réseau permettant au jeu de fonctionner et de réagir avec l'autre joueur
    :param game_scene: la scène du jeu
    :param thread: le thread dans lequel la fonction est appelé
    :param connection: la connexion avec l'autre joueur
    """

    # associe le type de packet avec la fonction correspondante
    game_methods: dict[Type["Packet"], Callable] = {
        packet.PacketChat: game_scene.network_on_chat,
        packet.PacketBoatPlaced: game_scene.network_on_boat_placed,
        packet.PacketBombPlaced: game_scene.network_on_bomb_placed,
        packet.PacketBombState: game_scene.network_on_bomb_state,
        packet.PacketQuit: game_scene.network_on_quit,
        packet.PacketAskSave: game_scene.network_on_ask_save,
        packet.PacketResponseSave: game_scene.network_on_response_save,
    }

    while True:
        # récupère le type de packet reçu
        data_type = Packet.type_from_connection(connection)

        if data_type is None:
            # s'il n'y a pas de donnée reçue, vérifie si le thread devrait s'arrêter, sinon ignore
            if thread.stopped: return
            continue

        # récupère les données du packet
        data = data_type.from_connection(connection)

        in_pyglet_context(
            game_methods[data_type], data  # récupère la methode relié à ce type de donnée
        )  # Appelle la méthode.

        if thread.stopped: return  # vérifie si le thread n'est pas censé s'arrêter
