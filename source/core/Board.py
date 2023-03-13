import numpy as np

from source.core import Boat
from source.core.enums import BombState
from source.core.error import InvalidBoatPosition, PositionAlreadyShot, InvalidBombPosition
from source.type import Point2D
from source.utils import copy_array_offset


class Board:
    """
    Représente la planche de jeu.
    Des bateaux et des bombes peuvent y être placé.
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
        Ajoute un bateau à la planche. Vérifie avant si la position est valide.
        :param boat: le bateau a placé
        :param position: la position du bateau sur la planche
        :raise: InvalidBoatPosition si la position du bateau est invalide
        """

        # récupère l'ancienne somme total de la grille matriciel
        board_matrice = self.boats.copy()
        board_matrice_sum_old: int = board_matrice.sum()
        board_matrice_max = np.max(board_matrice)

        # récupère la somme du bateau matriciel
        boat_matrice: np.array = boat.get_matrice(board_matrice_max+1)
        boat_matrice_sum: int = boat_matrice.sum()

        # ajoute la matrice du bateau à la matrice de la grille
        try:
            copy_array_offset(boat_matrice, board_matrice, offset=position)
        except ValueError:
            raise InvalidBoatPosition(boat, position)

        # récupère la nouvelle somme de la grille matricielle
        board_matrice_sum_new: int = board_matrice.sum()

        # si la somme de l'ancienne planche et de la matrice du bateau n'est pas égal à celle de la nouvelle grille,
        # alors le bateau n'est pas correctement placé (hors de la grille, par dessus un autre bateau, ...)
        if board_matrice_sum_old + boat_matrice_sum != board_matrice_sum_new:
            raise InvalidBoatPosition(boat, position)

        # sinon remplace l'ancienne matrice par la nouvelle
        self.boats = board_matrice

    def bomb(self, position: Point2D) -> BombState:
        """
        Place une bombe sur la grille
        :position: la position de la bombe
        :raise: PositionAlreadyShot si la bombe a déjà été placé ici, InvalidBombPosition si la position est invalide.
        """

        # si la bombe est bien dans les limites de la grille
        x, y = position
        if x >= self.width or y >= self.height: raise InvalidBombPosition(position)

        # si une bombe a déjà été placé ici
        if not self.bombs[y, x]: raise PositionAlreadyShot(position)

        # récupère l'ancienne somme de la matrice de la grille
        board_mat_old_sum = self.get_matrice().sum()

        # place la bombe dessus (False équivaut à placer une bombe)
        self.bombs[y, x] = False

        # récupère la nouvelle somme de la matrice de la grille
        board_mat_new = self.get_matrice()
        board_mat_new_sum = board_mat_new.sum()

        # si la somme de la grille matricielle est 0, alors il n'y a plus de bateau sur la grille
        if board_mat_new_sum == 0: return BombState.WON

        # récupère la différence entre l'ancienne et la nouvelle somme de la grille
        # si la somme a changé, alors un bateau a été touché.
        boat_touched: int = board_mat_old_sum - board_mat_new_sum

        # si aucun bateau n'a été touché, ignore
        if boat_touched == 0: return BombState.NOTHING

        # si le bateau a coulé (il n'y a plus de case correspondant à ce bateau)
        if not np.isin(boat_touched, board_mat_new): return BombState.SUNKEN

        # si le bateau a été touché partiellement
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
        :return: les bateaux et les bombes représentés sur une même matrice
        """

        # En multipliant la matrice des bombes par la matrice des bateaux,
        # tous les bateaux avec une bombe dessus seront mis à 0 puisqu'une bombe placée vaut "False".
        return self.boats * self.bombs

    def get_score(self) -> int:
        """
        :return: le score du joueur. (Nombre de bateau cassé)
        """

        boat_total: int = np.count_nonzero(self.boats)
        boat_left: int = np.count_nonzero(self.get_matrice())

        return boat_total - boat_left

    def to_json(self) -> dict:
        # converti en json les données
        return {
            "boats": self.boats.tolist(),
            "bombs": self.bombs.tolist()
        }

    @classmethod
    def from_json(cls, json_: dict) -> "Board":
        # charge à partir de json les données
        return Board(
            boats=np.array(json_["boats"], dtype=np.ushort),
            bombs=np.array(json_["bombs"], dtype=np.bool_)
        )

    def __copy__(self):
        # fait une copie de la grille
        return self.__class__(
            boats=self.boats.copy(),
            bombs=self.bombs.copy(),
        )
