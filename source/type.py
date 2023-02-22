from typing import Union, Callable, Any

Point2D = tuple[int, int]  # a 2D point
BBox = tuple[int, int, int, int]  # a boundary box
Percentage = float  # a percentage, represented as a number between 0 and 1
ColorRGB = tuple[int, int, int]  # a RGB Color
ColorRGBA = tuple[int, int, int, int]  # a RGBA Color

DistanceFunction = Callable[[Any], int]  # a function that return a distance
Distance = Union[int, Percentage, DistanceFunction]  # a distance, represented by a number, a percentage or a function
