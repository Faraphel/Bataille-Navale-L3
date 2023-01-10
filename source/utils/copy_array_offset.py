import numpy as np

from source.type import Point2D


def copy_array_offset(src: np.array, dst: np.array, offset: Point2D) -> None:
    """
    Copy a numpy array into another one with an offset
    :source: source array
    :dst: destination array
    :offset: the offset where to copy the array
    """
    row, column = offset
    width, height = src.shape
    dst[row:row + width, column:column + height] = src
