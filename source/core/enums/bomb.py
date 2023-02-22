from enum import Enum


class BombState(Enum):
    """
    This class represent the state of a bomb after being place on the board.
    """

    NOTHING = 0  # the bomb missed
    TOUCHED = 1  # the bomb touched a boat
    SUNKEN = 2  # the bomb touched the last part of a boat
    WON = 3  # the bomb sunk the last boat

    ERROR = 10  # the bomb could not be placed
