from typing import Union, Callable


Point2D = tuple[int, int]  # a 2D point
BBox = tuple[int, int, int, int]  # a boundary box
ColorRGB = tuple[int, int, int]  # a RGB Color
ColorRGBA = tuple[int, int, int, int]  # a RGBA Color

DistanceFunc = Callable[["BoxWidget"], int]  # a function that return a position / distance
Distance = Union[int, DistanceFunc]  # a position / distance, represented by a number or a function
