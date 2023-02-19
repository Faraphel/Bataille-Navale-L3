from . import _image_path
from .abc import Style

_image_path = _image_path + "button/"


class Button:
    class Style1(Style):
        normal = _image_path + "normal.png"
        click = _image_path + "clicking.png"
        hover = _image_path + "hovering.png"
