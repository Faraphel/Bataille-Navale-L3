from .abc import Style
from .type import Texture
from source.path import path_image

path = path_image / "popup"


class Popup:
    """
    Regroupe les textures des popups
    """

    class Style1(Style):
        background = Texture(path / "background.png")
