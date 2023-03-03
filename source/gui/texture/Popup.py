from . import path
from .abc import Style
from .type import Texture

path = path / "popup"


class Popup:
    class Style1(Style):
        background = Texture(path / "background.png")
