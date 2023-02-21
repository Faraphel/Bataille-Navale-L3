import socket
from typing import TYPE_CHECKING

import pyglet

from source.gui.scene.abc import Scene
from source.gui import widget, texture
from source.gui.widget.grid import GameGridAlly, GameGridEnemy
from source import core
from source.network.SocketType import SocketType

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
            GameGridAlly,

            x=75, y=0.25, width=0.35, height=0.5,

            boats_length=[5, 5, 4, 3, 2],

            grid_style=texture.Grid.Style1,
            boat_style=texture.Grid.Boat.Style1,
            rows=8, columns=8,

            background_batch=self.batch_grid_background,
            line_batch=self.batch_grid_line,
            cursor_batch=self.batch_grid_cursor,
            boat_batch=self.batch_grid_boat,
        )

        self.grid_enemy = self.add_widget(
            GameGridEnemy,

            x=lambda widget: widget.scene.window.width - 75 - widget.width, y=0.25, width=0.35, height=0.5,

            grid_style=texture.Grid.Style1,
            bomb_style=texture.Grid.Bomb.Style1,
            rows=8, columns=8,

            background_batch=self.batch_grid_background,
            line_batch=self.batch_grid_line,
            cursor_batch=self.batch_grid_cursor,
            bomb_batch=self.batch_grid_bomb
        )

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

            text="7",
            font_size=25,
            anchor_x="center", anchor_y="center",

            batch=self.batch_label,
        )

        self.score_enemy = self.add_widget(
            widget.Text,

            x=0.56, y=0.995,

            text="5",
            font_size=25,
            anchor_x="center", anchor_y="center",

            batch=self.batch_label,
        )

        self.chat_log = self.add_widget(
            widget.Text,

            x=10, y=70, width=0.5,

            text="FARAPHEL - HELLO BILLY\nLEO - HELLO BOLLO",
            anchor_x="left", anchor_y="baseline",
            multiline=True,

            batch=self.batch_label,
        )

        self.chat_input = self.add_widget(
            widget.Input,

            x=10, y=10, width=0.5, height=50,

            style=texture.Button.Style1,

            background_batch=self.batch_input_background,
            label_batch=self.batch_label,
        )

        def send_chat():
            connection.send(SocketType["CHAT"].value.to_bytes(1, "big"))
            connection.send(self.chat_input.text.encode())

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

        self.grid_enemy.draw()  # DEBUG
