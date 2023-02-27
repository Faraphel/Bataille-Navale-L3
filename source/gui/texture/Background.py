from . import path
from .abc import Style
from source.gui.texture.type import Texture

path = path / "background"


class Background(Style):
    main = Texture(path / "main.png")
    game = Texture(path / "game.png")
