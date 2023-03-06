from .abc import Style
from source.gui.texture.type import Texture
from source import path_image

path = path_image / "button"


class Button:
    class Style1(Style):
        normal = Texture(path / "normal.png")
        click = Texture(path / "clicking.png")
        hover = Texture(path / "hovering.png")
