from . import _image_path
from .abc import Style

_image_path = _image_path + "input/"


class Input:
    class Style1(Style):
        normal = _image_path + "normal.png"
        active = _image_path + "active.png"
        error = _image_path + "error.png"
