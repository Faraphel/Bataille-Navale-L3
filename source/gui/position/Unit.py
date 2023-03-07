from typing import Callable, TYPE_CHECKING

from source.gui.position import Value
from source.type import DistanceFunc

if TYPE_CHECKING:
    pass


class Unit:
    """
    Cette classe représente une unité de position (px, vw, ...).
    """

    def __init__(self, converter: Callable[[float], DistanceFunc]):
        self.converter = converter

    def __mul__(self, other: float):  # opérateur *
        """
        Lorsque que cet object est multiplié avec une valeur, renvoie un objet Value
        utilisant le convertisseur de l'unité.
        :param other: l'autre élément utilisé dans la multiplication.
        :return: l'objet Value
        """

        return Value(self.converter(other))

    def __rmul__(self, other):  # opérateur *, lorsque cet objet est situé à droite de l'opération
        return self.__mul__(other)
