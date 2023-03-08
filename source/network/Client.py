import json
import socket
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Callable

from source.path import path_save
from source.gui import scene
from source.network import game_network, handle_error
from source.network.packet import PacketUsername, PacketSettings, PacketHaveSaveBeenFound, PacketLoadOldSave
from source.utils import StoppableThread
from source.utils.thread import in_pyglet_context

if TYPE_CHECKING:
    from source.gui.window import Window


class Client(StoppableThread):
    """
    The thread executed on the person who join a room.
    """

    def __init__(self, window: "Window",
                 username: str,
                 ip_address: str,
                 port: int,
                 on_connexion_refused: Optional[Callable] = None,
                 **kw):
        super().__init__(**kw)

        self.window = window

        self.on_connexion_refused = on_connexion_refused

        self.username = username
        self.ip_address = ip_address
        self.port = port

    def run(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
                try:
                    connection.connect((self.ip_address, self.port))
                except ConnectionRefusedError:
                    # Appelle l'événement lorsque la connexion échoue
                    if self.on_connexion_refused is not None:
                        in_pyglet_context(self.on_connexion_refused)
                    return

                connection.settimeout(1)  # défini le timeout à 1 seconde

                # sauvegarde

                load_old_save: bool = False

                # attend que l'hôte indique s'il a trouvé une ancienne sauvegarde
                packet_save_found = PacketHaveSaveBeenFound.from_connection(connection).value

                if packet_save_found:
                    # si l'hôte a trouvé une ancienne sauvegarde, vérifier de notre côté également.

                    path_old_save: Optional[Path] = None
                    ip_address, _ = connection.getpeername()

                    for file in reversed(list(path_save.iterdir())):
                        # la liste est inversée dans le cas où le fichier est en localhost, afin que l'hôte
                        # prenne le fichier en -0.bn-save et le client en -1.bn-save
                        if file.stem.startswith(ip_address):
                            path_old_save = file
                            break

                    # envoie à l'hôte si l'on possède également la sauvegarde
                    PacketHaveSaveBeenFound(value=path_old_save is not None).send_data_connection(connection)

                    if path_old_save:
                        # si l'on possède la sauvegarde, attend que l'hôte confirme son utilisation

                        from source.gui.scene import GameWaitLoad
                        in_pyglet_context(self.window.set_scene, GameWaitLoad, path=path_old_save)

                        while True:
                            # attend la décision de l'hôte
                            try:
                                load_old_save = PacketLoadOldSave.from_connection(connection).value
                                break
                            except socket.timeout:
                                if self.stopped: return

                        if load_old_save:

                            # charge la sauvegarde
                            with open(path_old_save, "r", encoding="utf-8") as file:
                                save_data = json.load(file)

                # paramètres & jeu

                settings = PacketSettings.from_connection(connection)
                PacketUsername(username=self.username).send_data_connection(connection)
                enemy_username = PacketUsername.from_connection(connection).username

                if load_old_save:
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

                        boats_length=settings.boats_length,
                        name_ally=self.username,
                        name_enemy=enemy_username,
                        grid_width=settings.grid_width,
                        grid_height=settings.grid_height,
                        my_turn=not settings.host_start
                    )

                game_network(
                    thread=self,
                    connection=connection,
                    game_scene=game_scene,
                )

        except Exception as exception:
            handle_error(self.window, exception)
