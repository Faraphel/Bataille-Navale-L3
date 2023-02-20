from . import _image_path
from .abc import Style

_image_path = _image_path + "grid/"
_image_boat_path = _image_path + "boat/"


class Grid:
    class Style1(Style):
        background = _image_path + "background.png"

    class Boat:
        class Style1(Style):
            body = _image_boat_path + "body.png"
            edge = _image_boat_path + "edge.png"
            broken = _image_boat_path + "broken.png"
