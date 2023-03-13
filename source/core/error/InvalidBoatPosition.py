from source.core.Boat import Boat
from source.type import Point2D


class InvalidBoatPosition(Exception):
    """
    Erreur utilisée lorsque le bateau n'a pas pu être placé
    """

    def __init__(self, boat: Boat, position: Point2D):
        super().__init__(f"The boat {boat} can't be placed at {position}.")
