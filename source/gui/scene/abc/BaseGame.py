from abc import ABC
from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import right_content, h_percent, w_percent, w_full, h_full
from source.gui.scene.abc import Scene
from source.type import Point2D

if TYPE_CHECKING:
    from source.gui.window import Window


class BaseGame(Scene, ABC):
    def __init__(self, window: "Window",
                 boats_length: list,
                 name_ally: str,
                 name_enemy: str,

                 grid_width: int = None,
                 grid_height: int = None,
                 board_ally_data: dict = None,
                 board_enemy_data: dict = None,

                 history: list[bool, Point2D] = None,

                 **kwargs):

        super().__init__(window, **kwargs)

        self.boats_length = boats_length
        self.name_ally = name_ally
        self.name_enemy = name_enemy
        self.history: list[tuple[bool, Point2D]] = [] if history is None else history  # liste des bombes posées

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=w_full, height=h_full,

            image=texture.Background.game,
        )

        self.grid_ally = self.add_widget(
            widget.GameGrid,

            x=75, y=h_percent(25), width=w_percent(35), height=h_percent(50),

            boats_length=self.boats_length,

            grid_style=texture.Grid.Style1,
            boat_style=texture.Grid.Boat.Style1,

            rows=grid_height, columns=grid_width,
            board_data=board_ally_data
        )

        self.grid_enemy = self.add_widget(
            widget.GameGrid,

            x=right_content(75), y=h_percent(25), width=w_percent(35), height=h_percent(50),

            grid_style=texture.Grid.Style1,
            boat_style=texture.Grid.Boat.Style1,

            rows=grid_height, columns=grid_width,
            board_data=board_enemy_data
        )

        self.add_widget(
            widget.Text,

            x=w_percent(27), y=h_percent(99.5),

            text=self.name_ally,
            font_size=20,
            anchor_x="center", anchor_y="center"
        )

        self.add_widget(
            widget.Text,

            x=w_percent(73), y=h_percent(99.5),

            text=self.name_enemy,
            font_size=20,
            anchor_x="center", anchor_y="center"
        )

        self.score_ally = self.add_widget(
            widget.Text,

            x=w_percent(44), y=h_percent(99.5),

            text="0",
            font_size=25,
            anchor_x="center", anchor_y="center"
        )

        self.score_enemy = self.add_widget(
            widget.Text,

            x=w_percent(56), y=h_percent(99.5),

            text="0",
            font_size=25,
            anchor_x="center", anchor_y="center"
        )

        self.button_quit = self.add_widget(
            widget.Button,

            x=w_percent(85), y=0, width=w_percent(15), height=h_percent(10),

            label_text="Quitter",

            style=texture.Button.Style1
        )

    def _refresh_score_text(self):
        self.score_ally.text = str(self.grid_enemy.board.get_score())
        self.score_enemy.text = str(self.grid_ally.board.get_score())
