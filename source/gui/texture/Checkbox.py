from .abc import Style
from .type import Texture
from source import path_image

path = path_image / "checkbox"


class Checkbox:
    class Style1(Style):
        disabled = Texture(path / "disabled.png")
        enabled = Texture(path / "enabled.png")
