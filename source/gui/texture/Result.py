from .abc import Style
from .type import Animation
from source import path_image

path = path_image / "result"


class Result:
    class Style1(Style):
        victory = Animation((path / "victory").iterdir(), 0.04, False)
        defeat = Animation((path / "defeat").iterdir(), 0.04, False)
