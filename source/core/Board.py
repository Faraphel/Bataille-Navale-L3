import numpy as np

from source.core import Boat
from source.core.enums import Orientation, BombState
from source.core.error import InvalidBoatPosition, PositionAlreadyShot, InvalidBombPosition
from source.type import Point2D
from source.utils import copy_array_offset


class Board:
    """
    Represent a board for the game.
    Boat can be added and bomb can be placed.
    """

    __slots__ = ("width", "height", "boats", "bombs")

    def __init__(
            self,
            width: int = None,
            height: int = None,

            boats: np.array = None,
            bombs: np.array = None) -> None:

        if (width is None or height is None) and (boats is None or bombs is None):
            raise ValueError(f"{self.__class__}: width and height or boats and bombs should be set.")

        # associate the boats and the bombs to array
        self.boats: np.array = np.zeros((height, width), dtype=np.ushort) if boats is None else boats
        self.bombs: np.array = np.ones((height, width), dtype=np.bool_) if bombs is None else bombs

        # récupère la hauteur et la largeur
        self.height, self.width = self.boats.shape

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} width={self.width} height={self.height}>"

    def __str__(self) -> str:
        return str(self.get_matrice())

    def add_boat(self, boat: Boat, position: Point2D) -> None:
        """
        Add a boat to the board. Check before if the position is valid.
        :boat: the boat to add
        :position: the position where to add the boat
        :raise: InvalidBoatPosition if the boat position is not valid
        """

        # get the old board matrice sum
        board_matrice = self.boats.copy()
        board_matrice_sum_old: int = board_matrice.sum()
        board_matrice_max = np.max(board_matrice)

        # get the sum of the boat
        boat_matrice: np.array = boat.get_matrice(board_matrice_max+1)
        boat_matrice_sum: int = boat_matrice.sum()

        # add the boat to the board matrice
        try:
            copy_array_offset(boat_matrice, board_matrice, offset=position)
        except ValueError:
            raise InvalidBoatPosition(boat, position)

        #  get the new board matrice sum
        board_matrice_sum_new: int = board_matrice.sum()

        # if the sum of the old board plus the boat sum is different from the new board sum,
        # then the boat have been incorrectly placed (overlapping, outside of bounds, ...)
        if board_matrice_sum_old + boat_matrice_sum != board_matrice_sum_new:
            raise InvalidBoatPosition(boat, position)

        # otherwise accept the boat in the boats dict
        self.boats = board_matrice

    def bomb(self, position: Point2D) -> BombState:
        """
        Hit a position on the board
        :position: the position where to shoot
        :raise: PositionAlreadyShot if the position have already been shot before
        """

        # if the bomb is inside the board
        x, y = position
        if x >= self.width or y >= self.height: raise InvalidBombPosition(position)

        # if this position have already been shot
        if not self.bombs[y, x]: raise PositionAlreadyShot(position)

        # get the old board matrice
        board_mat_old_sum = self.get_matrice().sum()

        # place the bomb (setting the position to False cause the matrice multiplication to remove the boat if any)
        self.bombs[y, x] = False

        # get the new board matrice
        board_mat_new = self.get_matrice()
        board_mat_new_sum = board_mat_new.sum()

        # if the board sum is 0, then there is no boat left on the board
        if board_mat_new_sum == 0: return BombState.WON

        # get the difference between the old and new board sum.
        # if the board sum changed, then the difference is the number of the boat that have been hit
        boat_touched: int = board_mat_old_sum - board_mat_new_sum

        # if no boat have been touched, ignore
        if boat_touched == 0: return BombState.NOTHING

        # if the boat have sinked (no more tile with the boat on it)
        if not np.isin(boat_touched, board_mat_new): return BombState.SUNKEN

        # if the boat have been touched, but without sinking
        return BombState.TOUCHED

    def remove_bomb(self, cell: Point2D):
        """
        Retire une bombe de la matrice
        :param cell: cellule de la bombe
        """
        x, y = cell
        self.bombs[y, x] = True

    def clear_bombs(self):
        """
        Retire toutes les bombes de la planche
        """
        self.bombs = np.ones(self.bombs.shape)

    def get_matrice(self) -> np.array:
        """
        :return: the boats and bombs represented as a matrice
        """

        return self.boats * self.bombs  # Remove the position that have been bombed

    def get_score(self) -> int:
        """
        :return: le score du joueur. (Nombre de bateau cassé)
        """

        boat_total: int = np.count_nonzero(self.boats)
        boat_left: int = np.count_nonzero(self.get_matrice())

        return boat_total - boat_left

    def to_json(self) -> dict:
        return {
            "boats": self.boats.tolist(),
            "bombs": self.bombs.tolist()
        }

    @classmethod
    def from_json(cls, json_: dict) -> "Board":
        return Board(
            boats=np.array(json_["boats"], dtype=np.ushort),
            bombs=np.array(json_["bombs"], dtype=np.bool_)
        )

    def __copy__(self):
        return self.__class__(
            boats=self.boats.copy(),
            bombs=self.bombs.copy(),
        )
