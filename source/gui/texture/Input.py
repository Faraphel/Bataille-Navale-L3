from . import path
from .abc import Style

path = path / "input"


class Input:
    class Style1(Style):
        normal = path / "normal.png"
        active = path / "active.png"
        error = path / "error.png"
