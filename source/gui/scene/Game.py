from typing import TYPE_CHECKING

import pyglet

from source.gui.scene.abc import Scene
from source.gui import widget
from source import core

if TYPE_CHECKING:
    from source.gui.window import Window


class Game(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        texture_input_normal = pyglet.image.load("assets/image/input/normal.png")
        texture_input_active = pyglet.image.load("./assets/image/input/active.png")
        texture_input_error = pyglet.image.load("./assets/image/input/error.png")

        texture_button_normal = pyglet.image.load("./assets/image/button/normal.png")
        texture_button_hover = pyglet.image.load("./assets/image/button/hovering.png")
        texture_button_click = pyglet.image.load("./assets/image/button/clicking.png")

        texture_game_background = pyglet.image.load("./assets/image/background/game.png")

        texture_grid_background = pyglet.image.load("./assets/image/grid/background.png")

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=1.0, height=1.0,

            image=texture_game_background,
        )

        self.grid_ally = self.add_widget(
            widget.GameGrid,

            x=75, y=0.25, width=0.35, height=0.5,

            texture_background=texture_grid_background,
            rows=8, columns=8,
        )

        self.grid_enemy = self.add_widget(
            widget.GameGrid,

            x=lambda widget: widget.scene.window.width - 75 - widget.width, y=0.25, width=0.35, height=0.5,

            texture_background=texture_grid_background,
            rows=8, columns=8,
        )

        self.name_ally = self.add_widget(
            widget.Text,

            x=0.27, y=0.995,

            text="Raphael",
            font_size=20,
            anchor_x="center", anchor_y="center",
        )

        self.name_enemy = self.add_widget(
            widget.Text,

            x=0.73, y=0.995,

            text="Leo",
            font_size=20,
            anchor_x="center", anchor_y="center",
        )

        self.score_ally = self.add_widget(
            widget.Text,

            x=0.44, y=0.995,

            text="7",
            font_size=25,
            anchor_x="center", anchor_y="center"
        )

        self.score_enemy = self.add_widget(
            widget.Text,

            x=0.56, y=0.995,

            text="5",
            font_size=25,
            anchor_x="center", anchor_y="center"
        )

        self.chat_log = self.add_widget(
            widget.Text,

            x=10, y=70, width=0.5,

            text="FARAPHEL - HELLO BILLY\nLEO - HELLO BOLLO",
            anchor_x="left", anchor_y="baseline",
            multiline=True
        )

        self.chat_input = self.add_widget(
            widget.Input,

            x=10, y=10, width=0.5, height=50,

            texture_normal=texture_input_normal,
            texture_active=texture_input_active,
            texture_error=texture_input_error,
        )
        
        self.button_save = self.add_widget(
            widget.Button,

            x=0.7, y=0, width=0.15, height=0.1,

            label_text="Sauvegarder",

            texture_normal=texture_button_normal,
            texture_hover=texture_button_hover,
            texture_click=texture_button_click
        )

        self.button_quit = self.add_widget(
            widget.Button,

            x=0.85, y=0, width=0.15, height=0.1,
            
            label_text="Quitter",

            texture_normal=texture_button_normal,
            texture_hover=texture_button_hover,
            texture_click=texture_button_click
        )

        self.board_ally = core.Board(rows=8, columns=8)
        self.board_enemy = core.Board(rows=8, columns=8)

    def on_draw(self):
        self.background.draw()

        self.grid_ally.draw()
        self.grid_enemy.draw()

        self.name_ally.draw()
        self.name_enemy.draw()

        self.score_ally.draw()
        self.score_enemy.draw()

        self.chat_log.draw()
        self.chat_input.draw()

        self.button_save.draw()
        self.button_quit.draw()
