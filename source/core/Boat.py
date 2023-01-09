import numpy as np

from source.core.enums import Orientation


class Boat:
    __slots__ = ("orientation", "length")

    def __init__(self, length: int, orientation: Orientation):
        self.orientation = orientation
        self.length = length

    def get_matrice(self, value: int = 1) -> np.array:
        """
        :return: the boat represented as a matrice
        """
        return np.full(
            (1, self.length) if self.orientation == Orientation.HORIZONTAL else
            (self.length, 1),
            value,
            dtype=np.ushort
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} orientation={self.orientation}, length={self.length}>"


if __name__ == "__main__":
    print(Boat(5, Orientation.VERTICAL).get_matrice())
