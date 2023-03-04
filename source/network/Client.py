import socket
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

from source import path_save
from source.gui import scene
from source.network import game_network
from source.network.packet import PacketUsername, PacketSettings, PacketHaveSaveBeenFound, PacketLoadOldSave
from source.utils import StoppableThread
from source.utils.thread import in_pyglet_context

if TYPE_CHECKING:
    from source.gui.window import Window


class Client(StoppableThread):
    """
    The thread executed on the person who join a room.
    """

    def __init__(self, window: "Window", username: str, ip_address: str, port: int, **kw):
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

            # sauvegarde

            # attend que l'hôte indique s'il a trouvé une ancienne sauvegarde
            packet_save_found = PacketHaveSaveBeenFound.from_connection(connection)

            if packet_save_found.value:
                # si l'hôte a trouvé une ancienne sauvegarde, vérifier de notre côté également.

                path_old_save: Optional[Path] = None
                ip_address, _ = connection.getpeername()

                for file in path_save.iterdir():
                    if file.stem == ip_address:
                        path_old_save = file
                        break

                # envoie à l'hôte si l'on possède également la sauvegarde
                PacketHaveSaveBeenFound(value=path_old_save is not None).send_data_connection(connection)

                if path_old_save:
                    # si l'on possède la sauvegarde, attend que l'hôte confirme son utilisation

                    from source.gui.scene import GameWaitLoad
                    in_pyglet_context(self.window.set_scene, GameWaitLoad)

                    while True:
                        # attend la décision de l'hôte
                        try:
                            load_old_save = PacketLoadOldSave.from_connection(connection)
                            break
                        except socket.timeout:
                            if self.stopped: return

                    print("accept load", load_old_save)

                    if load_old_save.value:
                        ...
                        # TODO: Charger nos données

            # paramètres & jeu

            settings: Any = PacketSettings.from_connection(connection)
            PacketUsername(username=self.username).send_data_connection(connection)
            packet_username = PacketUsername.from_connection(connection)

            game_scene = in_pyglet_context(
                self.window.set_scene,
                scene.Game,

                thread=self,
                connection=connection,

                boats_length=settings.boats_length,
                name_ally=self.username,
                name_enemy=packet_username.username,
                grid_width=settings.grid_width,
                grid_height=settings.grid_height,
                my_turn=not settings.host_start
            )

            game_network(
                thread=self,
                connection=connection,
                game_scene=game_scene,
            )
