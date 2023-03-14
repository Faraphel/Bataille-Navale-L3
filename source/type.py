from typing import Union, Callable


Point2D = tuple[int, int]  # un point 2D
BBox = tuple[int, int, int, int]  # une boîte de collision
ColorRGB = tuple[int, int, int]  # une couleur RGB
ColorRGBA = tuple[int, int, int, int]  # une couleur RGBA

DistanceFunc = Callable[["BoxWidget"], int]  # une fonction renvoyant une position / distance
Distance = Union[int, DistanceFunc]  # une position / distance sous la forme d'un nombre ou d'une fonction
