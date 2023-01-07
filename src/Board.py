import numpy as np

from src import Boat
from src.enum import Orientation, BombState
from src.error import InvalidBoatPosition, PositionAlreadyShot
from src.utils import copy_array_offset


class Board:
    __slots__ = ("width", "height", "_boats", "_bombs")

    def __init__(self, width: int, height: int = None) -> None:
        self.width: int = width
        self.height: int = width if height is None else height
        self._boats: dict[Boat, tuple[int, int]] = {}  # associate the boats to their position
        self._bombs: np.array = np.ones((self.width, self.height), dtype=np.bool_)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} width={self.width}, height={self.height}>"

    def __str__(self) -> str:
        return str(self.get_matrice())

    def add_boat(self, boat: Boat, position: tuple[int, int]) -> None:
        """
        Add a boat to the board. Check before if the position is valid.
        :boat: the boat to add
        :position: the position where to add the boat
        :raise: InvalidBoatPosition if the boat position is not valid
        """

        # get the sum of the boat
        boat_sum: int = boat.get_matrice().sum()

        # get the old board matrice sum
        board_mat: np.array = self.get_matrice()
        board_mat_sum_old: int = board_mat.sum()

        # add the boat to the board matrice
        copy_array_offset(boat.get_matrice(), board_mat, offset=position)

        #  get the new board matrice sum
        board_mat_sum_new: int = board_mat.sum()

        # if the sum of the old board plus the boat sum is different from the new board sum,
        # then the boat have been incorrectly placed (overlapping, outside of bounds, ...)
        if board_mat_sum_old + boat_sum != board_mat_sum_new: raise InvalidBoatPosition(boat, position)

        # otherwise accept the boat in the boats dict
        self._boats[boat] = position

    def remove_boat(self, boat: Boat) -> None:
        """
        Remove a boat from the boat dict
        """
        self._boats.pop(boat)

    def bomb(self, position: tuple[int, int]) -> BombState:
        """
        Hit a position on the board
        :position: the position where to shoot
        :raise: PositionAlreadyShot if the position have already been shot before
        """
        # if this position have already been shot
        if not self._bombs[position]: raise PositionAlreadyShot(position)

        # get the old board matrice
        board_mat_old_sum = self.get_matrice().sum()

        # place the bomb (setting the position to False cause the matrice multiplication to remove the boat if any)
        self._bombs[position] = False

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

    def get_matrice(self) -> np.array:
        """
        :return: the boat represented as a matrice
        """
        board = np.zeros((self.width, self.height), dtype=np.ushort)

        for index, (boat, position) in enumerate(self._boats.items(), start=1):
            # Paste the boat into the board at the correct position.
            # The boat is represented by a number representing its order in the boats list
            copy_array_offset(boat.get_matrice(value=index), board, offset=position)

        board *= self._bombs  # Remove the position that have been bombed

        return board


if __name__ == "__main__":
    board = Board(5)
    board.add_boat(Boat(3, Orientation.VERTICAL), (0, 4))
    board.add_boat(Boat(4, Orientation.HORIZONTAL), (4, 1))
    print(board.bomb((4, 1)))
    print(board.bomb((4, 2)))
    print(board.bomb((4, 3)))
    print(board.bomb((4, 4)))
    print(board)


