from .abc import Style
from .type import Texture
from source import path_image

path = path_image / "replay"


class Replay:
    class Style1(Style):
        previous = Texture(path / "previous.png")
        next = Texture(path / "next.png")
