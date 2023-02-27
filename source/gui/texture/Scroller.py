from . import path
from .abc import Style
from .type import Texture

path = path / "scroller"


class Scroller:
    class Style1(Style):
        background = Texture(path / "background.png")
        cursor = Texture(path / "cursor.png")
