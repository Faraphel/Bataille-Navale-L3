from .abc import Style
from .type import Texture
from source import path_image

path = path_image / "popup"


class Popup:
    class Style1(Style):
        background = Texture(path / "background.png")
