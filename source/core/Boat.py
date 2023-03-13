import numpy as np

from source.core.enums import Orientation


class Boat:
    """
    Représente un bateau.
    Il peut être ajouté à une grille.
    """

    __slots__ = ("orientation", "length")

    def __init__(self, length: int, orientation: Orientation):
        self.orientation = orientation
        self.length = length

    def __repr__(self):
        return f"<{self.__class__.__name__} orientation={self.orientation}, length={self.length}>"

    def get_matrice(self, value: int = 1) -> np.array:
        """
        Représente le bateau sous la forme d'une matrice
        :return: le bateau sous la forme d'une matrice
        """
        return np.full(
            (1, self.length) if self.orientation == Orientation.HORIZONTAL else
            (self.length, 1),
            value,
            dtype=np.ushort
        )

    def to_json(self) -> dict:
        # converti le bateau en json
        return {
            "length": self.length,
            "orientation": self.orientation.to_json(),
        }

    @classmethod
    def from_json(cls, json_: dict) -> "Boat":
        # charge le bateau à partir de json
        return Boat(
            length=json_["length"],
            orientation=Orientation.from_json(json_["orientation"]),
        )


if __name__ == "__main__":
    print(Boat(5, Orientation.VERTICAL).get_matrice())
