from typing import Union, Callable, Any

Point2D = tuple[int, int]
BBox = tuple[int, int, int, int]
Percentage = float  # a percentage, represented as a number between 0 and 1

DistanceFunction = Callable[[Any], int]  # a function that return a distance
# a distance, represented either by a whole number, a percentage or a function
Distance = Union[Percentage, int, DistanceFunction]
