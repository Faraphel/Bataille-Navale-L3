from . import path
from .abc import Style

path = path / "checkbox"


class Checkbox:
    class Style1(Style):
        disabled = path / "disabled.png"
        enabled = path / "enabled.png"
