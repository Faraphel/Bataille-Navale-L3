from . import _image_path
from .abc import Style

_image_path = _image_path + "checkbox/"


class Checkbox:
    class Style1(Style):
        disabled = _image_path + "disabled.png"
        enabled = _image_path + "enabled.png"
