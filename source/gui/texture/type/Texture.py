from pathlib import Path

import pyglet

from source.gui.texture.type.abc import TextureType


class Texture(TextureType):
    """
    Représente une simple texture
    """

    def __init__(self, path: Path):
        self.path = path

    def __get__(self, instance, owner) -> pyglet.image.AbstractImage:
        return self.get_texture(self.path)
