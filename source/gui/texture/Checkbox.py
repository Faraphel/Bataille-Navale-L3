from . import path
from .abc import Style
from .type import Texture

path = path / "checkbox"


class Checkbox:
    class Style1(Style):
        disabled = Texture(path / "disabled.png")
        enabled = Texture(path / "enabled.png")
