from . import _image_path
from .abc import Style

_image_path = _image_path + "scroller/"


class Scroller:
    class Style1(Style):
        background = _image_path + "background.png"
        cursor = _image_path + "cursor.png"
