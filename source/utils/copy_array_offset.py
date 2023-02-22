import numpy as np

from source.type import Point2D


def copy_array_offset(src: np.array, dst: np.array, offset: Point2D) -> None:
    """
    Copy a numpy array into another one with an offset
    :param src: source array
    :param dst: destination array
    :param offset: the offset where to copy the array
    """
    column, row = offset
    width, height = src.shape
    dst[row:row + width, column:column + height] = src
