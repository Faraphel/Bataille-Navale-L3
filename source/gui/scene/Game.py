import socket
from typing import TYPE_CHECKING

from source.core.enums import BombState
from source.core.error import InvalidBombPosition, PositionAlreadyShot
from source.gui.scene import GameResult
from source.gui.scene.abc import Scene
from source.gui import widget, texture, scene
from source import core
from source.network.packet import PacketChat, PacketBombPlaced, PacketBoatPlaced, PacketBombState, PacketQuit
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
                 grid_width: int,
                 grid_height: int,
                 my_turn: bool,

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
            bomb_style=texture.Grid.Bomb.Style1,
            rows=self.grid_height, columns=self.grid_width
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
            bomb_style=texture.Grid.Bomb.Style1,
            rows=self.grid_height, columns=self.grid_width
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

        self.board_ally = core.Board(rows=self.grid_height, columns=self.grid_width)
        self.board_enemy = core.Board(rows=self.grid_height, columns=self.grid_width)

        self._my_turn = my_turn  # is it the player turn ?
        self._boat_ready_ally: bool = False  # does the player finished placing his boat ?
        self._boat_ready_enemy: bool = False  # does the opponent finished placing his boat ?
        self._boat_broken_ally: int = 0
        self._boat_broken_enemy: int = 0

        self._refresh_turn_text()

    # function

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

    def quit(self):
        PacketQuit().send_connection(self.connection)

        self.thread.stop()
        from source.gui.scene import MainMenu
        self.window.set_scene(MainMenu)

    def game_end(self, won: bool):
        self.window.add_scene(GameResult, game_scene=self, won=won)

    def chat_new_message(self, author: str, content: str):
        message: str = f"[{author}] - {content}"
        self.chat_log.text += "\n" + message

        self._refresh_chat_box()

    # property

    @property
    def boat_broken_ally(self):
        return self._boat_broken_ally

    @boat_broken_ally.setter
    def boat_broken_ally(self, boat_broken_ally: int):
        self._boat_broken_ally = boat_broken_ally
        self.score_ally.text = str(self._boat_broken_ally)

    @property
    def boat_broken_enemy(self):
        return self._boat_broken_enemy

    @boat_broken_enemy.setter
    def boat_broken_enemy(self, boat_broken_enemy: int):
        self._boat_broken_enemy = boat_broken_enemy
        self.score_enemy.text = str(self._boat_broken_enemy)

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

    # network

    def network_on_chat(self, packet: PacketChat):
        self.chat_new_message(self.name_enemy, packet.message)

    def network_on_boat_placed(self, packet: PacketBoatPlaced):
        self.boat_ready_enemy = True

    def network_on_bomb_placed(self, packet: PacketBombPlaced):
        try:
            # essaye de poser la bombe sur la grille alliée
            bomb_state = self.grid_ally.board.bomb(packet.position)
        except (InvalidBombPosition, PositionAlreadyShot):
            # si une erreur se produit, signale l'erreur
            bomb_state = BombState.ERROR
            # l'opposant va rejouer, ce n'est donc pas notre tour
            self.my_turn = False
        else:
            # si la bombe a bien été placé, affiche-la sur la grille visuel allié
            self.grid_ally.place_bomb(packet.position, bomb_state.success)
            # c'est à notre tour si l'opposant à loupé sa bombe
            self.my_turn = not bomb_state.success

        # envoie le résultat à l'autre joueur
        PacketBombState(position=packet.position, bomb_state=bomb_state).send_connection(self.connection)

        if bomb_state.success:
            # si la bombe a touché un bateau, incrémente le score
            self.boat_broken_enemy += 1

        if bomb_state is BombState.WON:
            # si l'ennemie à gagner, alors l'on a perdu
            self.game_end(won=False)
            return True  # coupe la connexion

    def network_on_bomb_state(self, packet: PacketBombState):
        if packet.bomb_state is BombState.ERROR:
            # si une erreur est survenue, on rejoue
            self.my_turn = True
            return

        # on rejoue uniquement si la bombe à toucher
        self.my_turn = packet.bomb_state.success

        if packet.bomb_state.success:
            # si la bombe à toucher, incrémente le score
            self.boat_broken_ally += 1

        # place la bombe sur la grille ennemie visuelle
        self.grid_enemy.place_bomb(packet.position, packet.bomb_state.success)

        if packet.bomb_state is BombState.WON:
            # si cette bombe a touché le dernier bateau, alors l'on a gagné
            self.game_end(won=True)
            return True  # coupe la connexion

    def network_on_quit(self, packet: PacketQuit):
        self.thread.stop()
        from source.gui.scene import GameError
        self.window.set_scene(GameError, text="L'adversaire a quitté la partie.")

    # event

    def on_resize_after(self, width: int, height: int):
        self._refresh_chat_box()
