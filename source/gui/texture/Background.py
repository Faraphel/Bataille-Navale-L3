from . import path
from .abc import Style


path = path / "background"


class Background(Style):
    main = path / "main.png"
    game = path / "game.png"
