from . import path
from .abc import Style

path = path / "result"


class Result:
    class Style1(Style):
        victory = (path / "victory").iterdir(), 0.04, False
        defeat = (path / "defeat").iterdir(), 0.04, False
