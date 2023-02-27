from . import path
from .abc import Style
from .type import Animation

path = path / "result"


class Result:
    class Style1(Style):
        victory = Animation((path / "victory").iterdir(), 0.04, False)
        defeat = Animation((path / "defeat").iterdir(), 0.04, False)
