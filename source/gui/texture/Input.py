from .abc import Style
from .type import Texture
from source import path_image

path = path_image / "input"


class Input:
    class Style1(Style):
        normal = Texture(path / "normal.png")
        active = Texture(path / "active.png")
        error = Texture(path / "error.png")
