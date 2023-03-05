import json
import socket
from typing import TYPE_CHECKING

from source import path_save
from source.core.enums import BombState
from source.core.error import InvalidBombPosition, PositionAlreadyShot
from source.gui.scene import GameResult
from source.gui.scene.abc import Scene
from source.gui import widget, texture, scene
from source.network.packet import PacketChat, PacketBombPlaced, PacketBoatPlaced, PacketBombState, PacketQuit, \
    PacketAskSave, PacketResponseSave
from source.type import Point2D
from source.utils import StoppableThread

if TYPE_CHECKING:
    from source.gui.window import Window


class Game(Scene):
    def __init__(self, window: "Window",
                 thread: StoppableThread,
                 connection: socket.socket,

                 boats_length: list,
                 name_ally: str,
                 name_enemy: str,
                 my_turn: bool,

                 grid_width: int = None,
                 grid_height: int = None,
                 board_ally_data: dict = None,
                 board_enemy_data: dict = None,

                 **kwargs):
        super().__init__(window, **kwargs)

        self.thread = thread
        self.connection = connection
        self.boats_length = boats_length
        self.name_ally = name_ally
        self.name_enemy = name_enemy
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=1.0, height=1.0,

            image=texture.Background.game,
        )

        self.grid_ally = self.add_widget(
            widget.GameGrid,

            x=75, y=0.25, width=0.35, height=0.5,

            boats_length=self.boats_length,

            grid_style=texture.Grid.Style1,
            boat_style=texture.Grid.Boat.Style1,
            rows=self.grid_height, columns=self.grid_width,

            board_data=board_ally_data
        )

        def board_ally_ready(widget):
            self.boat_ready_ally = True
            PacketBoatPlaced().send_connection(connection)

        self.grid_ally.add_listener("on_all_boats_placed", board_ally_ready)

        self.grid_enemy = self.add_widget(
            widget.GameGrid,

            x=lambda widget: widget.scene.window.width - 75 - widget.width, y=0.25, width=0.35, height=0.5,

            grid_style=texture.Grid.Style1,
            boat_style=texture.Grid.Boat.Style1,
            rows=self.grid_height, columns=self.grid_width,

            board_data=board_enemy_data
        )

        def board_enemy_bomb(widget, cell: Point2D):
            if not (self.boat_ready_ally and self.boat_ready_enemy): return
            if not self.my_turn: return

            PacketBombPlaced(position=cell).send_connection(connection)
            self.my_turn = False

        self.grid_enemy.add_listener("on_request_place_bomb", board_enemy_bomb)

        self.add_widget(
            widget.Text,

            x=0.27, y=0.995,

            text=self.name_ally,
            font_size=20,
            anchor_x="center", anchor_y="center"
        )

        self.add_widget(
            widget.Text,

            x=0.73, y=0.995,

            text=self.name_enemy,
            font_size=20,
            anchor_x="center", anchor_y="center"
        )

        self.score_ally = self.add_widget(
            widget.Text,

            x=0.44, y=0.995,

            text="0",
            font_size=25,
            anchor_x="center", anchor_y="center"
        )

        self.score_enemy = self.add_widget(
            widget.Text,

            x=0.56, y=0.995,

            text="0",
            font_size=25,
            anchor_x="center", anchor_y="center"
        )

        self.chat_log = self.add_widget(
            widget.Text,

            x=10, y=45, width=0.4,

            text="",
            anchor_x="left", anchor_y="bottom",
            multiline=True
        )

        self.chat_input = self.add_widget(
            widget.Input,

            x=10, y=10, width=0.5, height=30,

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

            x=0.7, y=0, width=0.15, height=0.1,

            label_text="Sauvegarder",

            style=texture.Button.Style1
        )

        def ask_save(widget, x, y, button, modifiers):
            if not (self._boat_ready_ally and self._boat_ready_enemy):
                self.chat_new_message("System", "Veuillez poser vos bateaux avant de sauvegarder.")
                return

            # TODO: Pas spam le bouton
            PacketAskSave().send_connection(self.connection)
            self.chat_new_message("System", "demande de sauvegarde envoyé.")

        self.button_save.add_listener("on_click_release", ask_save)

        self.button_quit = self.add_widget(
            widget.Button,

            x=0.85, y=0, width=0.15, height=0.1,
            
            label_text="Quitter",

            style=texture.Button.Style1
        )

        self.button_quit.add_listener("on_click_release",
                                      lambda *_: self.window.add_scene(scene.GameQuit, game_scene=self))

        self.label_state = self.add_widget(
            widget.Text,

            x=0.5, y=0.15,

            anchor_x="center",

            font_size=20
        )

        self._my_turn = my_turn  # is it the player turn ?
        self._boat_ready_ally: bool = False   # does the player finished placing his boat ?
        self._boat_ready_enemy: bool = False  # does the opponent finished placing his boat ?

        if len(boats_length) == 0:  # s'il n'y a pas de bateau à placé
            self._boat_ready_ally = True  # défini l'état de notre planche comme prête
            PacketBoatPlaced().send_connection(connection)  # indique à l'adversaire que notre planche est prête

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

    def _refresh_score_text(self):
        self.score_ally.text = str(self.grid_enemy.board.get_score())
        self.score_enemy.text = str(self.grid_ally.board.get_score())

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

    # function

    def to_json(self) -> dict:
        return {
            "my_turn": self.my_turn,
            "grid_ally": self.grid_ally.board.to_json(),
            "grid_enemy": self.grid_enemy.board.to_json(),
        }

    @classmethod
    def from_json(cls,
                  data: dict,

                  window: "Window",
                  thread: StoppableThread,
                  connection: socket.socket,
                  name_ally: str,
                  name_enemy: str) -> "Game":

        return cls(
            window=window,
            thread=thread,
            connection=connection,
            boats_length=[],
            name_ally=name_ally,
            name_enemy=name_enemy,

            my_turn=data["my_turn"],

            board_ally_data=data["grid_ally"],
            board_enemy_data=data["grid_enemy"]
        )

    def save(self, value: bool):
        self.chat_new_message(
            "System",
            "Sauvegarde de la partie..." if value else "Sauvegarde de la partie refusé."
        )
        if not value: return

        ip_address, port = self.connection.getpeername()
        # Le nom du fichier est l'IP de l'opposent, suivi d'un entier indiquant si c'est à notre tour ou non.
        # Cet entier permet aux localhost de toujours pouvoir sauvegarder et charger sans problème.
        filename: str = f"{ip_address}-{int(self.my_turn)}.bn-save"

        with open(path_save / filename, "w", encoding="utf-8") as file:
            json.dump(self.to_json(), file, ensure_ascii=False, indent=4)

    def game_end(self, won: bool):
        self.window.add_scene(GameResult, game_scene=self, won=won)  # affiche le résultat
        self.thread.stop()  # coupe la connexion

    def chat_new_message(self, author: str, content: str):
        message: str = f"[{author}] - {content}"
        self.chat_log.text += "\n" + message

        self._refresh_chat_box()

    # network

    def network_on_chat(self, packet: PacketChat):
        self.chat_new_message(self.name_enemy, packet.message)

    def network_on_boat_placed(self, packet: PacketBoatPlaced):
        self.boat_ready_enemy = True

    def network_on_bomb_placed(self, packet: PacketBombPlaced):
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

        # envoie le résultat à l'autre joueur
        PacketBombState(position=packet.position, bomb_state=bomb_state).send_connection(self.connection)

        self._refresh_score_text()  # le score a changé, donc rafraichi son texte

        if bomb_state is BombState.WON:
            # si l'ennemie à gagner, alors l'on a perdu
            self.game_end(won=False)

    def network_on_bomb_state(self, packet: PacketBombState):
        if packet.bomb_state is BombState.ERROR:
            # si une erreur est survenue, on rejoue
            self.my_turn = True
            return

        # on rejoue uniquement si la bombe à toucher
        self.my_turn = packet.bomb_state.success

        self._refresh_score_text()  # le score a changé, donc rafraichi son texte

        # place la bombe sur la grille ennemie visuelle
        self.grid_enemy.place_bomb(packet.position, force_touched=packet.bomb_state.success)

        if packet.bomb_state is BombState.WON:
            # si cette bombe a touché le dernier bateau, alors l'on a gagné
            self.game_end(won=True)

    def network_on_quit(self, packet: PacketQuit):
        self.thread.stop()  # coupe la connexion

        from source.gui.scene import GameError
        self.window.set_scene(GameError, text="L'adversaire a quitté la partie.")

    def network_on_ask_save(self, packet: PacketAskSave):
        from source.gui.scene import GameSave
        self.window.add_scene(GameSave, game_scene=self)

    def network_on_response_save(self, packet: PacketResponseSave):
        self.save(value=packet.value)

    # event

    def on_resize_after(self, width: int, height: int):
        self._refresh_chat_box()
