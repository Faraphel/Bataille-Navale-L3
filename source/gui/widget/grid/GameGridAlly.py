from copy import copy
from typing import TYPE_CHECKING, Type

import pyglet
import numpy as np

from source.core.enums import Orientation
from source.core.error import InvalidBoatPosition
from source.gui import texture
from source.gui.sprite import Sprite
from source.gui.texture.abc import Style
from source.gui.widget.grid.abc import GameGrid
from source.core import Board, Boat
from source.type import Point2D, ColorRGB
from source.utils import dict_filter_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class GameGridAlly(GameGrid):
    def __init__(self, scene: "Scene",

                 rows: int,
                 columns: int,

                 grid_style: Type[Style],
                 boat_style: Type[Style],

                 boats_length: list[int],
                 preview_color: ColorRGB = (150, 255, 150),

                 **kwargs):
        self.cell_sprites: dict[Point2D, "Sprite"] = {}

        super().__init__(scene, rows, columns, grid_style, **kwargs)

        self.boats_length = boats_length  # the list of the size of the boats to place
        self.preview_color = preview_color

        self.board = Board(rows=self.rows, columns=self.columns)
        self.orientation: Orientation = Orientation.HORIZONTAL

        self._boat_kwargs = dict_filter_prefix("boat_", kwargs)
        self.boat_style = boat_style

        self.add_listener("on_click_release", self.on_click_release)
        self.add_listener("on_hover", lambda rel_x, rel_y: self.preview_boat(self.get_cell_from_rel(rel_x, rel_y)))

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

    def display_board(self, board: Board, preview: bool = False):
        self.cell_sprites: dict[Point2D, "Sprite"] = {}

        matrice = board.get_matrice()
        max_boat: int = matrice.max()

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
                img=self.boat_style.get(form),
                **self._boat_kwargs
            )
            sprite.rotation = rotation * 90

            if preview and value == max_boat:  # if in preview and it is the latest boat
                sprite.color = self.preview_color   # make the image more greenish

            self.cell_sprites[(x, y)] = sprite

        self._refresh_size()

    def swap_orientation(self):
        self.orientation = (
            Orientation.HORIZONTAL if self.orientation is Orientation.VERTICAL else
            Orientation.VERTICAL
        )

    def place_boat(self, cell: Point2D):
        if len(self.boats_length) == 0: return

        try:
            self.board.add_boat(
                Boat(self.boats_length[0], orientation=self.orientation),
                cell
            )
        except InvalidBoatPosition: pass  # if the boat can't be placed, ignore

        else:  # if the boat have been placed
            self.boats_length.pop(0)  # remove the boat from the list of boat to place

        self.display_board(self.board)

    def preview_boat(self, cell: Point2D):
        if len(self.boats_length) == 0: return

        try:
            preview_board = copy(self.board)
            preview_board.add_boat(
                Boat(self.boats_length[0], orientation=self.orientation),
                cell
            )

        except InvalidBoatPosition: self.display_board(self.board)  # if the boat can't be placed, ignore
        else: self.display_board(preview_board, preview=True)

    def on_click_release(self, rel_x: int, rel_y: int, button: int, modifiers: int):
        cell = self.get_cell_from_rel(rel_x, rel_y)

        match button:
            case pyglet.window.mouse.RIGHT:
                self.swap_orientation()
                self.preview_boat(cell)

            case pyglet.window.mouse.LEFT:
                self.place_boat(cell)

    def draw(self):
        self.background.draw()
        for sprite in self.cell_sprites.values(): sprite.draw()
        self.cursor.draw()
        for line in self.lines: line.draw()
