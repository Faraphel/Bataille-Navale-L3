from typing import TYPE_CHECKING

import pyglet
import numpy as np

from source.core.enums import Orientation
from source.core.error import InvalidBoatPosition
from source.gui import texture
from source.gui.sprite import Sprite
from source.gui.widget.grid.abc import GameGrid
from source.core import Board, Boat
from source.type import Point2D
from source.utils import dict_filter_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class GameGridAlly(GameGrid):
    def __init__(self, scene: "Scene", boats_length: list[int], **kwargs):
        self.cell_sprites: dict[Point2D, "Sprite"] = {}

        super().__init__(scene, **kwargs)

        self.orientation: Orientation = Orientation.HORIZONTAL
        self.boats_length = boats_length  # the list of the size of the boats to place
        self.board = Board(rows=self.rows, columns=self.columns)

        self._cell_kwargs = dict_filter_prefix("cell_", kwargs)

    # refresh
    def _refresh_size(self):
        super()._refresh_size()

        for (x, y), sprite in self.cell_sprites.items():

            # calcul des décalages à cause de la rotation qui est faite par rapport à l'origine de l'image

            offset_x = 0 if sprite.rotation <= 90 else self.cell_width
            offset_y = self.cell_height if 90 <= sprite.rotation <= 180 else 0

            width, height = (
                (self.cell_width, self.cell_height) if sprite.rotation % 180 == 0 else
                (self.cell_height, self.cell_width)
            )

            sprite.x = self.x + (x * self.cell_width) + offset_x
            sprite.y = self.y + (y * self.cell_height) + offset_y
            sprite.width = width
            sprite.height = height

    def _refresh_board(self):
        self.cell_sprites: dict[Point2D, "Sprite"] = {}

        matrice = self.board.get_matrice()

        for (y, x), value in np.ndenumerate(matrice):
            if value == 0: continue

            # calcul de la forme et de la rotation de cette cellule du bateau

            form, rotation = (
                # corps
                ("body", 0) if 0 < y < (self.rows-1) and matrice[y-1, x] == matrice[y+1, x] == value else  # colonne
                ("body", 1) if 0 < x < (self.columns-1) and matrice[y, x-1] == matrice[y, x+1] == value else  # ligne

                # bordure
                ("edge", 0) if 0 < y and matrice[y-1, x] == value else  # bas
                ("edge", 1) if 0 < x and matrice[y, x-1] == value else  # droite
                ("edge", 2) if y < (self.rows-1) and matrice[y+1, x] == value else  # haut
                ("edge", 3) if x < (self.columns-1) and matrice[y, x+1] == value else  # gauche

                # aucune bordure (bateau de taille 1)
                ("solo", 0)
            )

            sprite = Sprite(
                img=texture.Grid.Boat.Style1.get(form),
                **self._cell_kwargs
            )
            sprite.rotation = rotation * 90

            self.cell_sprites[(x, y)] = sprite

        self._refresh_size()

    def swap_orientation(self):
        self.orientation = (
            Orientation.HORIZONTAL if self.orientation is Orientation.VERTICAL else
            Orientation.VERTICAL
        )

    def place_boat(self, x, y):
        rel_x, rel_y = x - self.x, y - self.y
        cell_x, cell_y = self.get_cell_from_rel(rel_x, rel_y)

        try:
            self.board.add_boat(
                Boat(self.boats_length[0], orientation=self.orientation),
                (cell_x, cell_y)
            )

        except InvalidBoatPosition:
            return

        else:
            self.boats_length.pop(0)

        self._refresh_board()

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        super().on_mouse_release(x, y, button, modifiers)

        if button == pyglet.window.mouse.RIGHT: self.swap_orientation()
        if button == pyglet.window.mouse.LEFT: self.place_boat(x, y)

    def draw(self):
        super().draw()
        for sprite in self.cell_sprites.values():
            sprite.draw()
