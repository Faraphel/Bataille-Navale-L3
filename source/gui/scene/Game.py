import json
import socket
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from source.gui.position import vw, vh
from source.path import path_save, path_history
from source.core.enums import BombState
from source.core.error import InvalidBombPosition, PositionAlreadyShot
from source.gui.scene import GameResult
from source.gui.scene.abc import BaseGame
from source.gui import widget, texture, scene, media
from source.network.packet import *
from source.type import Point2D
from source.utils import StoppableThread

if TYPE_CHECKING:
    from source.gui.window import Window


class Game(BaseGame):
    """
    Scène sur laquelle deux joueurs s'affrontent en réseau
    """

    def __init__(self, window: "Window",
                 thread: StoppableThread,
                 connection: socket.socket,

                 my_turn: bool,

                 **kwargs):
        super().__init__(window, **kwargs)

        self.thread = thread
        self.connection = connection

        def board_ally_ready(widget):
            self.boat_ready_ally = True
            PacketBoatPlaced().send_connection(connection)

        self.grid_ally.add_listener("on_all_boats_placed", board_ally_ready)
        self.grid_ally.add_listener("on_boat_placed", lambda *_: media.SoundEffect.placed.play())

        def board_enemy_bomb(widget, cell: Point2D):
            if not (self.boat_ready_ally and self.boat_ready_enemy): return
            if not self.my_turn: return

            PacketBombPlaced(position=cell).send_connection(connection)
            self.my_turn = False

        self.grid_enemy.add_listener("on_request_place_bomb", board_enemy_bomb)

        self.chat_log = self.add_widget(
            widget.Text,

            x=10, y=45, width=40*vw,

            text="",
            anchor_x="left", anchor_y="bottom",
            multiline=True
        )

        self.chat_input = self.add_widget(
            widget.Input,

            x=10, y=10, width=50*vw, height=30,

            type_regex=".{0,60}",

            style=texture.Button.Style1
        )

        def send_chat(widget):
            text: str = widget.text
            widget.text = ""

            self.chat_new_message(self.name_ally, text)
            PacketChat(message=text).send_connection(connection)

        self.chat_input.add_listener("on_enter", send_chat)
        
        self.button_save = self.add_widget(
            widget.Button,

            x=55*vw, y=0, width=15*vw, height=10*vh,

            label_text="Sauvegarder",

            style=texture.Button.Style1
        )

        def ask_save(widget, x, y, button, modifiers):
            if not (self._boat_ready_ally and self._boat_ready_enemy):
                self.chat_new_message("System", "Veuillez poser vos bateaux avant de sauvegarder.", system=True)
                return

            PacketAskSave().send_connection(self.connection)
            self.chat_new_message("System", "demande de sauvegarde envoyé.", system=True)

        self.button_save.add_listener("on_click_release", ask_save)

        self.button_quit.add_listener(
            "on_click_release",
            lambda *_: self.window.add_scene(scene.GameQuit, game_scene=self)
        )

        self.label_state = self.add_widget(
            widget.Text,

            x=50*vw, y=15*vh,

            anchor_x="center",

            font_size=20
        )

        self._my_turn = my_turn  # est-ce au tour de ce joueur ?
        self._boat_ready_ally: bool = False   # le joueur à t'il fini de placer ses bateaux ?
        self._boat_ready_enemy: bool = False  # l'opposant à t'il fini de placer ses bateaux ?

        if len(self.boats_length) == 0:  # s'il n'y a pas de bateau à placé
            self._boat_ready_ally = True  # défini l'état de notre planche comme prête
            PacketBoatPlaced().send_connection(connection)  # indique à l'adversaire que notre planche est prête

        self.save_cooldown: Optional[datetime] = None

        media.SoundAmbient.sea.play_safe(loop=True)

        self._refresh_turn_text()
        self._refresh_score_text()

    # refresh

    def _refresh_chat_box(self):
        # supprime des messages jusqu'à ce que la boite soit plus petite que un quart de la fenêtre
        while self.chat_log.label.content_height > (self.window.height / 4):
            chat_logs: list[str] = self.chat_log.text.split("\n")
            self.chat_log.text = "\n".join(chat_logs[1:])

        # ajuste la boite de message pour être collé en bas
        self.chat_log.label.y = self.chat_log.y + self.chat_log.label.content_height

    def _refresh_turn_text(self):
        self.label_state.text = (
            "Placer vos bateaux" if not self.boat_ready_ally else
            "L'adversaire place ses bateaux..." if not self.boat_ready_enemy else
            "Placer vos bombes" if self.my_turn else
            "L'adversaire place ses bombes..."
        )

    # property

    @property
    def my_turn(self):
        return self._my_turn

    @my_turn.setter
    def my_turn(self, my_turn: bool):
        self._my_turn = my_turn
        self._refresh_turn_text()

    @property
    def boat_ready_ally(self):
        return self._boat_ready_ally

    @boat_ready_ally.setter
    def boat_ready_ally(self, boat_ready_ally: bool):
        self._boat_ready_ally = boat_ready_ally
        self._refresh_turn_text()

    @property
    def boat_ready_enemy(self):
        return self._boat_ready_enemy

    @boat_ready_enemy.setter
    def boat_ready_enemy(self, boat_ready_enemy: bool):
        self._boat_ready_enemy = boat_ready_enemy
        self._refresh_turn_text()

    # fonction

    def to_json(self) -> dict:
        return {
            "name_ally": self.name_ally,
            "name_enemy": self.name_enemy,
            "my_turn": self.my_turn,
            "grid_ally": self.grid_ally.board.to_json(),
            "grid_enemy": self.grid_enemy.board.to_json(),
            "history": self.history,
        }

    @classmethod
    def from_json(cls,
                  data: dict,

                  window: "Window",
                  thread: StoppableThread,
                  connection: socket.socket) -> "Game":

        return cls(
            window=window,
            thread=thread,
            connection=connection,
            boats_length=[],

            name_ally=data["name_ally"],
            name_enemy=data["name_enemy"],

            my_turn=data["my_turn"],

            board_ally_data=data["grid_ally"],
            board_enemy_data=data["grid_enemy"],

            history=data["history"]
        )

    def get_save_suffix(self) -> str:
        # Le suffix est un entier indiquant si c'est à notre tour ou non.
        # Cet entier permet aux localhost de toujours pouvoir sauvegarder et charger sans problème.
        ip_address, port = self.connection.getpeername()
        return f"-{int(self.my_turn)}" if ip_address == "127.0.0.1" else ""

    @property
    def save_path(self) -> Path:
        # renvoie le chemin du fichier de sauvegarde
        ip_address, port = self.connection.getpeername()

        return path_save / (
                ip_address +
                self.get_save_suffix() +
                ".bn-save"
        )

    @property
    def history_path(self):
        # renvoie le chemin du fichier d'historique
        return path_history / (
            datetime.now().strftime("%Y-%m-%d %H-%M-%S") +
            self.get_save_suffix() +
            ".bn-history"
        )

    def save_to_path(self, path: Path):
        # enregistre la partie dans un fichier
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.to_json(), file, ensure_ascii=False)

    def save(self, value: bool):
        # fonction de callback lorsque l'adversaire accepte ou refuse la demande de sauvegarde
        self.chat_new_message(
            "System",
            "Sauvegarde de la partie..." if value else "Sauvegarde de la partie refusé.",
            system=True
        )
        if not value: return

        self.save_to_path(self.save_path)

    def game_end(self, won: bool):
        # envoie notre planche à l'adversaire
        PacketBoatsData(boats=self.grid_ally.board.boats).send_data_connection(self.connection)
        packet_boats = PacketBoatsData.from_connection(self.connection)
        self.grid_enemy.board.boats = packet_boats.boats

        # s'il existe une ancienne sauvegarde, efface la
        self.save_path.unlink(missing_ok=True)

        # sauvegarde cette partie dans l'historique
        self.save_to_path(self.history_path)

        self.window.add_scene(GameResult, game_scene=self, won=won)  # affiche le résultat
        self.thread.stop()

    def chat_new_message(self, author: str, content: str, system: bool = False):
        # envoie un message dans le chat
        deco_left, deco_right = "<>" if system else "[]"
        message: str = f"{deco_left}{author}{deco_right} - {content}"
        self.chat_log.text += "\n" + message

        self._refresh_chat_box()

    # network

    def network_on_chat(self, packet: PacketChat):
        # lorsque l'adversaire envoie un message
        self.chat_new_message(self.name_enemy, packet.message)

    def network_on_boat_placed(self, packet: PacketBoatPlaced):
        # lorsque l'adversaire indique avoir placé tous ses bateaux
        self.boat_ready_enemy = True

    def network_on_bomb_placed(self, packet: PacketBombPlaced):
        # lorsque l'opposant pose une bombe
        if self.my_turn: return  # l'opposant ne peut pas jouer si c'est notre tour

        try:
            # essaye de poser la bombe sur la grille alliée
            bomb_state = self.grid_ally.place_bomb(packet.position)
        except (InvalidBombPosition, PositionAlreadyShot):
            # si une erreur se produit, signale l'erreur
            bomb_state = BombState.ERROR
            # l'opposant va rejouer, ce n'est donc pas notre tour
            self.my_turn = False
        else:
            # c'est à notre tour si l'opposant à loupé sa bombe
            self.my_turn = not bomb_state.success
            # sauvegarde la bombe dans l'historique
            self.history.append((False, packet.position))

            # joue la musique associée à ce mouvement
            match bomb_state:
                case BombState.NOTHING: media.SoundEffect.missed.play()
                case BombState.TOUCHED: media.SoundEffect.touched.play()
                case BombState.SUNKEN: media.SoundEffect.sunken.play()
                case BombState.WON: media.SoundEffect.defeat.play()

        # envoie le résultat à l'autre joueur
        PacketBombState(position=packet.position, bomb_state=bomb_state).send_connection(self.connection)

        self._refresh_score_text()  # le score a changé, donc rafraichi son texte

        if bomb_state is BombState.WON:
            # si l'ennemie à gagner, alors l'on a perdu
            self.game_end(won=False)

    def network_on_bomb_state(self, packet: PacketBombState):
        # lorsque l'adversaire indique si la bombe à touché ou non
        if packet.bomb_state is BombState.ERROR:
            # si une erreur est survenue, on rejoue
            self.my_turn = True
            return

        # on rejoue uniquement si la bombe à toucher
        self.my_turn = packet.bomb_state.success

        self._refresh_score_text()  # le score a changé, donc rafraichi son texte

        # place la bombe sur la grille ennemie visuelle
        self.grid_enemy.place_bomb(packet.position, force_touched=packet.bomb_state.success)

        # sauvegarde la bombe dans l'historique
        self.history.append((True, packet.position))

        # joue la musique associée à ce mouvement
        match packet.bomb_state:
            case BombState.NOTHING: media.SoundEffect.missed.play()
            case BombState.TOUCHED: media.SoundEffect.touched.play()
            case BombState.SUNKEN: media.SoundEffect.sunken.play()
            case BombState.WON: media.SoundEffect.victory.play()

        if packet.bomb_state is BombState.WON:
            # si cette bombe a touché le dernier bateau, alors l'on a gagné
            self.game_end(won=True)

    def network_on_quit(self, packet: PacketQuit):
        # lorsque l'adversaire souhaite quitter
        self.thread.stop()  # coupe la connexion

        from source.gui.scene import GameError
        self.window.set_scene(GameError, text="L'adversaire a quitté la partie.")

    def network_on_ask_save(self, packet: PacketAskSave):
        # lorsque l'opposant souhaite sauvegarder
        now = datetime.now()

        if self.save_cooldown is not None:  # si un cooldown est défini
            if self.save_cooldown + timedelta(seconds=40) >= now:
                # si l'action à déjà été faite dans les 40 dernières secondes, ignore la requête de sauvegarde
                return

        self.save_cooldown = now

        from source.gui.scene import GameSave
        self.window.add_scene(GameSave, game_scene=self)

    def network_on_response_save(self, packet: PacketResponseSave):
        self.save(value=packet.value)

    # event

    def on_resize_after(self, width: int, height: int):
        self._refresh_chat_box()
