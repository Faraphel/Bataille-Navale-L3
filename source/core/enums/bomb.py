from enum import Enum


class BombState(Enum):
    NOTHING = 0
    TOUCHED = 1
    SUNKEN = 2
    WON = 3

    ERROR = 10
