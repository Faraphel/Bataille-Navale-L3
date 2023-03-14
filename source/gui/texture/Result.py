from .abc import Style
from .type import Animation
from source.path import path_image

path = path_image / "result"


class Result:
    """
    Regroupe les animations de fin de jeu
    """

    class Style1(Style):
        victory = Animation((path / "victory").iterdir(), 0.04, False)
        defeat = Animation((path / "defeat").iterdir(), 0.04, False)
