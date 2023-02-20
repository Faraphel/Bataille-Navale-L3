from typing import TYPE_CHECKING

import pyglet
import numpy as np

from source.core.enums import Orientation
from source.gui import texture
from source.gui.sprite import Sprite
from source.gui.widget.grid.abc import GameGrid
from source.core import Board, Boat

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class GameGridAlly(GameGrid):
    def __init__(self, scene: "Scene", boats_length: tuple[int, ...], **kwargs):
        super().__init__(scene, **kwargs)

        self.orientation = False
        self.boats_length = boats_length  # the list of the size of the boats to place

        self.add_listener("on_hover",
                          lambda rel_x, rel_y: self.preview_boat(self.get_cell_from_rel(rel_x, rel_y), self.boats_length[0]))

        self.cell_sprites: list["Sprite"] = []
        self.boat_sprites_preview: list["Sprite"] = []

    def draw_board(self, board: Board):
        matrice = board.get_matrice()

        for (y, x), value in np.ndenumerate(matrice):
            if value == 0: continue

            # calcul de la forme et de la rotation de cette cellule du bateau

            rotation = 0

            # body

            if 0 < y < (self.rows-1) and matrice[y-1, x] == matrice[y+1, x] == value:  # haut et bas
                form = "body"

            elif 0 < x < (self.columns-1) and matrice[y, x-1] == matrice[y, x+1] == value:  # droite et gauche
                form = "body"
                rotation = 90

            # edge

            elif 0 < y and matrice[y-1, x] == value:  # haut
                form = "edge"

            elif y < (self.rows-1) and matrice[y+1, x] == value:  # bas
                form = "edge"
                rotation = 180

            elif 0 < x and matrice[y, x-1] == value:  # gauche
                form = "edge"
                rotation = 90

            elif x < (self.columns-1) and matrice[y, x+1] == value:  # droite
                form = "edge"
                rotation = 270

            else:  # 1 piece boat
                form = "solo"

            # calcul des décalages à cause de la rotation qui est faite par rapport à l'origine de l'image
            offset_x = 0 if rotation < 180 else self.cell_width
            offset_y = self.cell_height if 90 <= rotation <= 180 else 0
            width = self.cell_width if rotation % 180 == 0 else self.cell_height
            height = self.cell_height if rotation % 180 == 0 else self.cell_width

            s = Sprite(
                img=texture.Grid.Boat.Style1.get(form),

                x=self.x + (x * self.cell_width) + offset_x,
                y=self.y + (y * self.cell_height) + offset_y,
                width=int(width),
                height=int(height),
            )
            s.rotation = rotation
            s.draw()

    def preview_boat(self, cell: tuple[int, int], length: int):
        cell_x, cell_y = cell

        self.boat_sprites_preview = []

        for i in range(length):
            self.boat_sprites_preview.append(
                Sprite(
                    img=texture.Grid.Boat.Style1.body,

                    x=self.x + (cell_x * self.cell_width) + ((self.cell_width * i) if not self.orientation else 0),
                    y=self.y + (cell_y * self.cell_height) + ((self.cell_height * i) if self.orientation else 0),
                    width=int(self.cell_width),
                    height=int(self.cell_height),
                )
            )

    def swap_orientation(self):
        self.orientation = not self.orientation

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        super().on_mouse_release(x, y, button, modifiers)
        if button == pyglet.window.mouse.RIGHT: self.swap_orientation()

    def on_draw(self):
        b = Board(rows=self.rows, columns=self.columns)
        b.add_boat(Boat(length=4, orientation=Orientation.VERTICAL), (0, 0))
        b.add_boat(Boat(length=5, orientation=Orientation.HORIZONTAL), (0, 1))
        b.add_boat(Boat(length=2, orientation=Orientation.HORIZONTAL), (0, 6))
        self.draw_board(b)
        for boat_sprite in self.boat_sprites_preview: boat_sprite.draw()
