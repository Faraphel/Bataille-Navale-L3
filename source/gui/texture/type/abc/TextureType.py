from abc import ABC, abstractmethod
from pathlib import Path

import pyglet


class TextureType(ABC):
    loaded_image: dict[Path, pyglet.image.AbstractImage] = {}

    @classmethod
    def get_texture(cls, path: Path) -> pyglet.image.AbstractImage:
        if (texture := cls.loaded_image.get(path)) is None:
            texture = pyglet.image.load(path)
            cls.loaded_image[path] = texture

        return texture

    @abstractmethod
    def __get__(self, instance, owner) -> pyglet.image.AbstractImage:
        pass
