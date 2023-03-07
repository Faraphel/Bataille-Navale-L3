from typing import TYPE_CHECKING

from source.type import DistanceFunc

if TYPE_CHECKING:
    from source.gui.widget.abc import BoxWidget


class Value:
    """
    Une valeur utilisée pour calculer la position des objets.
    Elle utilise une fonction permettant à partir d'un widget, d'obtenir une position dans la fenêtre
    """

    def __init__(self, calc: DistanceFunc):
        self.calc = calc  # fonction calculant la position depuis la taille d'un widget

    def __add__(self, other) -> "Value":  # opérateur +
        """
        Créer un nouvel objet Value correspondant à l'addition des deux opérandes
        :param other: l'autre élément utilisé dans la multiplication.
        :return: le nouvel objet Value
        """
        return self.__class__(lambda widget: self.calc(widget) + other.calc(widget))

    def __radd__(self, other):  # opérateur +, lorsque cet objet est situé à droite de l'opération
        return self.__add__(other)

    def __sub__(self, other) -> "Value":  # opérateur -
        """
        Créer un nouvel objet Value correspondant à la soustraction des deux opérandes
        :param other: l'autre élément utilisé dans la multiplication.
        :return: le nouvel objet Value
        """
        return self.__class__(lambda widget: self.calc(widget) - other.calc(widget))

    def __rsub__(self, other):  # opérateur -, lorsque cet objet est situé à droite de l'opération
        # similaire à __sub__, mais c'est cette valeur qui est soustraite à l'autre
        return self.__class__(lambda widget: other.calc(widget) - self.calc(widget))

    def __call__(self, widget: "BoxWidget") -> int:  # lorsque cet objet est appelé comme une fonction
        """
        Calcul pour le widget en paramètre la valeur associé.
        :param widget: Le widget à utiliser pour les calculs
        :return: la position correspondant à ce widget.
        """
        return self.calc(widget)
