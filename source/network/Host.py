import json
import socket
from pathlib import Path
from typing import TYPE_CHECKING, Optional
from threading import Condition

from source.path import path_save
from source.gui import scene
from source.network import game_network
from source.utils import StoppableThread
from source.utils.thread import in_pyglet_context
from source.network.packet import PacketUsername, PacketLoadOldSave, PacketHaveSaveBeenFound

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.network.packet import PacketSettings


class Host(StoppableThread):
    """
    The thread executed on the person who create a room.
    """

    def __init__(self, window: "Window", port: int, username: str, settings: "PacketSettings", **kw):
        super().__init__(**kw)

        self.window = window
        self.username = username
        self.settings = settings
        self.port = port

        self.condition_load = Condition()
        self.accept_load: bool = False

    def run(self) -> None:
        print("[Serveur] Thread démarré")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("", self.port))  # connecte le socket au port indiqué

            server.settimeout(1)  # défini le timeout à 1 seconde
            server.listen()  # écoute de nouvelle connexion

            while True:
                try:
                    connection, (ip_address, port) = server.accept()  # accepte la première connexion entrante
                    break  # sort de la boucle
                except socket.timeout:  # en cas de timeout
                    if self.stopped: return  # vérifie si le thread n'est pas censé s'arrêter
                    # sinon, réessaye

            print(f"[Serveur] Connecté avec {ip_address}")

            # ancienne sauvegarde

            path_old_save: Optional[Path] = None

            for file in path_save.iterdir():  # cherche une ancienne sauvegarde correspondant à l'ip de l'adversaire
                if file.stem.startswith(ip_address):
                    path_old_save = file
                    break

            # envoie à l'adversaire si une ancienne sauvegarde a été trouvée
            PacketHaveSaveBeenFound(value=path_old_save is not None).send_data_connection(connection)

            if path_old_save is not None:
                # si une ancienne sauvegarde a été trouvée, attend que l'adversaire confirme avoir également la save
                packet_save_found = PacketHaveSaveBeenFound.from_connection(connection).value

                # si l'adversaire à également la sauvegarde, demande à l'hôte de confirmer l'utilisation de la save
                if packet_save_found:

                    from source.gui.scene import GameLoad
                    in_pyglet_context(self.window.set_scene, GameLoad, path=path_old_save, thread_host=self)

                    with self.condition_load: self.condition_load.wait()  # attend que l'utilisateur choisisse l'option

                    try:
                        PacketLoadOldSave(value=self.accept_load).send_data_connection(connection)
                    except ConnectionResetError:
                        from source.gui.scene import GameError
                        in_pyglet_context(
                            self.window.set_scene,
                            GameError,
                            text="Perte de connexion avec l'adversaire"
                        )
                        return

                    if self.accept_load:

                        # charge la sauvegarde
                        with open(path_old_save, "r", encoding="utf-8") as file:
                            save_data = json.load(file)

            # paramètres et jeu

            self.settings.send_data_connection(connection)
            enemy_username = PacketUsername.from_connection(connection).username
            PacketUsername(username=self.username).send_data_connection(connection)

            if self.accept_load:
                game_scene = in_pyglet_context(
                    self.window.set_scene,
                    scene.Game.from_json,  # depuis le fichier json

                    data=save_data,

                    thread=self,
                    connection=connection
                )

            else:
                game_scene = in_pyglet_context(
                    self.window.set_scene,
                    scene.Game,

                    thread=self,
                    connection=connection,

                    boats_length=self.settings.boats_length,
                    name_ally=self.username,
                    name_enemy=enemy_username,
                    grid_width=self.settings.grid_width,
                    grid_height=self.settings.grid_height,
                    my_turn=self.settings.host_start
                )

            game_network(
                thread=self,
                connection=connection,
                game_scene=game_scene
            )

            # TODO: englober les threads de try sur ConnectionResetError pour ramener au menu d'erreur directement
            # au lieu de le faire manuellement à chaque fois
