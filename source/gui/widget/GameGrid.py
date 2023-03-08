from copy import copy
from typing import TYPE_CHECKING, Type

import numpy as np
import pyglet.shapes

from source.core import Board, Boat
from source.core.enums import Orientation, BombState
from source.core.error import InvalidBoatPosition
from source.gui.better_pyglet import Sprite
from source.gui.texture.abc import Style
from source.gui.widget.abc import BoxWidget
from source.type import Distance, Point2D
from source.utils import dict_filter_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class GameGrid(BoxWidget):
    """
    A widget that represent a game grid.
    """

    def __init__(self, scene: "Scene",

                 grid_style: Type[Style],
                 boat_style: Type[Style],

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,

                 boats_length: list[int] = None,

                 rows: int = None,
                 columns: int = None,
                 board_data: dict = None,

                 **kwargs):
        if (rows is None or columns is None) and board_data is None:
            raise ValueError(f"{self.__class__} object need to set rows and columns, or the board_data")

        self.cell_sprites: dict[Point2D, tuple["Sprite", hash]] = {}

        super().__init__(scene, x, y, width, height)

        self.group_cursor = pyglet.graphics.Group(order=1)
        self.group_line = pyglet.graphics.Group(order=2)

        # the list of the size of the boats to place
        self.boats_length = [] if boats_length is None else sorted(boats_length, reverse=True)

        # créer la planche du jeu
        self.board = Board(width=rows, height=columns) if board_data is None else Board.from_json(board_data)
        self.rows = self.board.height
        self.columns = self.board.width

        self.orientation: Orientation = Orientation.HORIZONTAL

        self._boat_kwargs = dict_filter_prefix("boat_", kwargs)
        self._bomb_kwargs = dict_filter_prefix("bomb_", kwargs)
        self.grid_style = grid_style
        self.boat_style = boat_style

        self.background = Sprite(
            img=grid_style.get("background"),
            batch=self.scene.batch,
            **dict_filter_prefix("background_", kwargs)
        )

        self.lines: list[pyglet.shapes.Line] = [
            pyglet.shapes.Line(
                0, 0, 0, 0,
                batch=self.scene.batch,
                group=self.group_line,
                **dict_filter_prefix("line_", kwargs)
            )
            for _ in range((self.columns - 1) + (self.rows - 1))
        ]

        self.cursor = pyglet.shapes.Rectangle(
            0, 0, 0, 0,
            color=(0, 0, 0, 100),
            batch=self.scene.batch,
            group=self.group_cursor
        )

        self.add_listener("on_click_release", lambda _, *args: self.on_click_release(*args))
        self.add_listener("on_hover_leave", lambda *_: self.hide_cursor())
        self.add_listener("on_hover", lambda _, *args: self._refresh_cursor(*args))

        self._refresh_size()
        self.refresh_board()

    def get_cell_from_rel(self, rel_x: int, rel_y: int) -> tuple[int, int]:
        """
        Return the cell of the grid from a point relative position
        """

        return (
            int((rel_x-1) / self.cell_width),
            int((rel_y-1) / self.cell_height)
        )

    # refresh

    def _refresh_size(self):
        self.background.x, self.background.y = self.xy
        self.background.width, self.background.height = self.size

        # lines

        for column, line in enumerate(self.lines[:self.columns - 1], start=1):
            line.x = self.x + self.cell_width * column
            line.x2 = line.x
            line.y = self.y
            line.y2 = self.y2

        for row, line in enumerate(self.lines[-self.rows + 1:], start=1):
            line.x = self.x
            line.x2 = self.x2
            line.y = self.y + self.cell_height * row
            line.y2 = line.y

        # sprites

        for (x, y), (sprite, hash_) in self.cell_sprites.items():
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

    def _refresh_cursor(self, rel_x: int, rel_y: int):
        cell_x, cell_y = self.get_cell_from_rel(rel_x, rel_y)

        self.cursor.x = self.x + cell_x * self.width / self.columns
        self.cursor.y = self.y + cell_y * self.height / self.rows
        self.cursor.width, self.cursor.height = self.cell_size

        self.preview_boat((cell_x, cell_y))  # display the preview of the boat on this cell

    # function

    def hide_cursor(self):
        self.cursor.width, self.cursor.height = 0, 0

    def refresh_board(self):
        # rafraichi l'affichage de la grille
        self.display_board(self.board)

    def display_board(self, board: Board, preview: bool = False):
        # remplacer par l'utilisation de board.boats ?

        matrice = board.boats
        max_boat: int = np.max(matrice)

        for (y, x), value in np.ndenumerate(matrice):
            bombed: bool = not board.bombs[y, x]  # cette case a déjà été attaqué si la valeur est "False".

            if value == 0 and not bombed:

                if (x, y) in self.cell_sprites:
                    self.cell_sprites.pop((x, y))

                continue  # ignore s'il n'y a ni bombe, ni bateau.

            # calcul de la forme et de la rotation de cette cellule du bateau

            form, rotation = (
                # bombe
                ("touched", 0) if bombed and value != 0 else
                ("missed", 0) if bombed else

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

            # si le bateau est le dernier placé et qu'on est en prévisualisation, change sa teinte.
            if preview and value == max_boat:
                form: str = f"preview_{form}"

            hash_new = hash((form, rotation))
            sprite_old, hash_old = self.cell_sprites.get((x, y), (None, None))

            if hash_old == hash_new:
                # si la texture n'a pas changé, ne rafraichi pas le sprite
                continue

            sprite = Sprite(
                img=self.boat_style.get(form),
                batch=self.scene.batch,
                **self._boat_kwargs
            )
            sprite.rotation = rotation * 90

            self.cell_sprites[x, y] = (sprite, hash_new)

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
        except InvalidBoatPosition:
            pass  # if the boat can't be placed, ignore

        else:  # if the boat have been placed
            self.boats_length.pop(0)  # remove the boat from the list of boat to place
            if len(self.boats_length) == 0:
                self.trigger_event("on_all_boats_placed")

        self.refresh_board()  # rafraichi l'affichage

    def preview_boat(self, cell: Point2D):
        if len(self.boats_length) == 0: return

        try:
            preview_board = copy(self.board)
            preview_board.add_boat(
                Boat(self.boats_length[0], orientation=self.orientation),
                cell
            )
        except InvalidBoatPosition:
            self.refresh_board()  # if the boat can't be placed, ignore

        else: self.display_board(preview_board, preview=True)

    def place_bomb(self, cell: Point2D, force_touched: bool = None) -> BombState:
        bomb_state = self.board.bomb(cell)

        if force_touched is not None:
            x, y = cell
            self.board.boats[y, x] = int(force_touched)

        self.refresh_board()
        return bomb_state

    def remove_bomb(self, cell: Point2D):
        # retire une bombe de la planche
        self.board.remove_bomb(cell)
        self.refresh_board()

    def on_click_release(self, rel_x: int, rel_y: int, button: int, modifiers: int):
        cell = self.get_cell_from_rel(rel_x, rel_y)

        match button:
            case pyglet.window.mouse.RIGHT:
                self.swap_orientation()
                self.preview_boat(cell)

            case pyglet.window.mouse.LEFT:
                self.place_boat(cell)
                self.trigger_event("on_request_place_bomb", cell)

    # property

    @property
    def cell_width(self) -> float:
        return self.width / self.columns

    @property
    def cell_height(self) -> float:
        return self.height / self.rows

    @property
    def cell_size(self) -> tuple[float, float]:
        return self.cell_width, self.cell_height

    # event

    def on_resize(self, width: int, height: int):
        self._refresh_size()
