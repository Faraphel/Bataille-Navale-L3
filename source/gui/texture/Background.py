from .abc import Style
from source.gui.texture.type import Texture
from source.path import path_image

path = path_image / "background"


class Background(Style):
    main = Texture(path / "main.png")
    game = Texture(path / "game.png")
