from . import path
from .abc import Style
from .type import Texture

path = path / "input"


class Input:
    class Style1(Style):
        normal = Texture(path / "normal.png")
        active = Texture(path / "active.png")
        error = Texture(path / "error.png")
