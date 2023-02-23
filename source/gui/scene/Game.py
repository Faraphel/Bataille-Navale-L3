import socket
from typing import TYPE_CHECKING

import pyglet

from source.gui.scene.abc import Scene
from source.gui import widget, texture
from source import core
from source.network.packet import PacketChat, PacketBombPlaced, PacketBoatPlaced
from source.type import Point2D

if TYPE_CHECKING:
    from source.gui.window import Window


class Game(Scene):
    def __init__(self, window: "Window", connection: socket.socket, **kwargs):
        super().__init__(window, **kwargs)

        self.connection = connection

        self.batch_label = pyglet.graphics.Batch()
        self.batch_button_background = pyglet.graphics.Batch()
        self.batch_input_background = pyglet.graphics.Batch()
        self.batch_grid_background = pyglet.graphics.Batch()
        self.batch_grid_line = pyglet.graphics.Batch()
        self.batch_grid_cursor = pyglet.graphics.Batch()
        self.batch_grid_boat = pyglet.graphics.Batch()
        self.batch_grid_bomb = pyglet.graphics.Batch()

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=1.0, height=1.0,

            image=texture.Background.game,
        )

        self.grid_ally = self.add_widget(
            widget.GameGrid,

            x=75, y=0.25, width=0.35, height=0.5,

            boats_length=[5, 5, 4, 3, 2],

            grid_style=texture.Grid.Style1,
            boat_style=texture.Grid.Boat.Style1,
            bomb_style=texture.Grid.Bomb.Style1,
            rows=8, columns=8,

            background_batch=self.batch_grid_background,
            line_batch=self.batch_grid_line,
            cursor_batch=self.batch_grid_cursor,
            boat_batch=self.batch_grid_boat,
            bomb_batch=self.batch_grid_bomb
        )

        def board_ally_ready():
            self.boat_ready_ally = True
            PacketBoatPlaced().send_connection(connection)

        self.grid_ally.add_listener("on_all_boats_placed", board_ally_ready)

        self.grid_enemy = self.add_widget(
            widget.GameGrid,

            x=lambda widget: widget.scene.window.width - 75 - widget.width, y=0.25, width=0.35, height=0.5,

            grid_style=texture.Grid.Style1,
            boat_style=texture.Grid.Boat.Style1,
            bomb_style=texture.Grid.Bomb.Style1,
            rows=8, columns=8,

            background_batch=self.batch_grid_background,
            line_batch=self.batch_grid_line,
            cursor_batch=self.batch_grid_cursor,
            boat_batch=self.batch_grid_boat,
            bomb_batch=self.batch_grid_bomb
        )

        def board_enemy_bomb(cell: Point2D):
            if not (self.boat_ready_ally and self.boat_ready_enemy): return
            if not self.my_turn: return
            PacketBombPlaced(position=cell).send_connection(connection)
            self.my_turn = False

        self.grid_enemy.add_listener("on_request_place_bomb", board_enemy_bomb)

        self.name_ally = self.add_widget(
            widget.Text,

            x=0.27, y=0.995,

            text="Raphael",
            font_size=20,
            anchor_x="center", anchor_y="center",

            batch=self.batch_label,
        )

        self.name_enemy = self.add_widget(
            widget.Text,

            x=0.73, y=0.995,

            text="Leo",
            font_size=20,
            anchor_x="center", anchor_y="center",

            batch=self.batch_label,
        )

        self.score_ally = self.add_widget(
            widget.Text,

            x=0.44, y=0.995,

            text="0",
            font_size=25,
            anchor_x="center", anchor_y="center",

            batch=self.batch_label,
        )

        self.score_enemy = self.add_widget(
            widget.Text,

            x=0.56, y=0.995,

            text="0",
            font_size=25,
            anchor_x="center", anchor_y="center",

            batch=self.batch_label,
        )

        self.chat_log = self.add_widget(
            widget.Text,

            x=10, y=35, width=0.5,

            text="",
            anchor_x="left",
            multiline=True,

            batch=self.batch_label,
        )

        self.chat_input = self.add_widget(
            widget.Input,

            x=10, y=10, width=0.5, height=30,

            style=texture.Button.Style1,

            background_batch=self.batch_input_background,
            label_batch=self.batch_label,
        )

        def send_chat():
            text = self.chat_input.text
            self.chat_input.text = ""

            self.chat_log.text += "\n" + text
            self.chat_log.label.y = self.chat_log.y + self.chat_log.label.content_height

            PacketChat(message=text).send_connection(connection)

        self.chat_input.add_listener("on_enter", send_chat)
        
        self.button_save = self.add_widget(
            widget.Button,

            x=0.7, y=0, width=0.15, height=0.1,

            label_text="Sauvegarder",

            style=texture.Button.Style1,

            background_batch=self.batch_button_background,
            label_batch=self.batch_label,
        )

        self.button_quit = self.add_widget(
            widget.Button,

            x=0.85, y=0, width=0.15, height=0.1,
            
            label_text="Quitter",

            style=texture.Button.Style1,

            background_batch=self.batch_button_background,
            label_batch=self.batch_label,
        )

        self.board_ally = core.Board(rows=8, columns=8)
        self.board_enemy = core.Board(rows=8, columns=8)

        self.my_turn: bool = False  # is it the player turn ?
        self.boat_ready_ally: bool = False  # does the player finished placing his boat ?
        self.boat_ready_enemy: bool = False  # does the opponent finished placing his boat ?
        self._boat_broken_ally: int = 0
        self._boat_broken_enemy: int = 0

    def boat_broken_ally(self):
        self._boat_broken_ally += 1
        self.score_ally.text = str(self._boat_broken_ally)

    def boat_broken_enemy(self):
        self._boat_broken_enemy += 1
        self.score_enemy.text = str(self._boat_broken_enemy)

    def on_draw(self):
        self.background.draw()

        self.batch_button_background.draw()
        self.batch_input_background.draw()
        self.batch_grid_background.draw()
        self.batch_grid_boat.draw()
        self.batch_grid_bomb.draw()
        self.batch_grid_line.draw()
        self.batch_grid_cursor.draw()

        self.batch_label.draw()
