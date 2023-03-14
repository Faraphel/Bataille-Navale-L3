from .abc import Style
from .type import Texture
from source.path import path_image

path = path_image / "checkbox"


class Checkbox:
    """
    Regroupe les textures des checkbox.
    """

    class Style1(Style):
        disabled = Texture(path / "disabled.png")
        enabled = Texture(path / "enabled.png")
