from . import path
from .abc import Style

path = path / "scroller"


class Scroller:
    class Style1(Style):
        background = path / "background.png"
        cursor = path / "cursor.png"
