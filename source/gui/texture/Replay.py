from . import path
from .abc import Style
from .type import Texture

path = path / "replay"


class Replay:
    class Style1(Style):
        previous = Texture(path / "previous.png")
        next = Texture(path / "next.png")
