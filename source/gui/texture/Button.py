from . import path
from .abc import Style

path = path / "button"


class Button:
    class Style1(Style):
        normal = path / "normal.png"
        click = path / "clicking.png"
        hover = path / "hovering.png"
