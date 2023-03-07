from .abc import Style
from .type import Texture
from source.path import path_image

path = path_image / "scroller"


class Scroller:
    class Style1(Style):
        background = Texture(path / "background.png")
        cursor = Texture(path / "cursor.png")
