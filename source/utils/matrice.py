import numpy as np

from source.type import Point2D


def copy_array_offset(src: np.array, dst: np.array, offset: Point2D) -> None:
    """
    Copie une matrice dans une autre matrice avec un décalage.
    :param src: la matrice source
    :param dst: la matrice de destination
    :param offset: le décalage avec lequel copier la matrice
    """
    column, row = offset
    width, height = src.shape
    dst[row:row + width, column:column + height] = src
