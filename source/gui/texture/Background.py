from . import _image_path
from .abc import Style


_image_path = _image_path + "background/"


class Background(Style):
    main = _image_path + "main.png"
    game = _image_path + "game.png"
