from .abc import Style
from source.gui.texture.type import Texture
from source.path import path_image

path = path_image / "background"


class Background(Style):
    """
    Regroupe les textures de fond
    """

    main = Texture(path / "main.png")

    settings = Texture(path / "settings.png")
    choice = Texture(path / "choice.png")
    time = Texture(path / "time.png")
    connexion = Texture(path / "connexion.png")

    game = Texture(path / "game.png")

    error = Texture(path / "error.png")
