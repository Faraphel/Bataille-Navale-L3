from enum import Enum


class BombState(Enum):
    """
    Cette classe représente les états d'une bombe après avoir été placé sur la grille.
    """

    NOTHING = 0  # la bombe a manqué
    TOUCHED = 1  # la bombe a touché un bateau
    SUNKEN = 2  # la bombe a coulé un bateau
    WON = 3  # la bombe a coulé le dernier bateau

    ERROR = -1  # la bombe n'a pas été placé

    @property
    def success(self):
        """
        :return: Vrai si une case a été touché
        """
        return self in [self.TOUCHED, self.SUNKEN, self.WON]
