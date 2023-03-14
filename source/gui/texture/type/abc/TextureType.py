from abc import ABC, abstractmethod
from pathlib import Path

import pyglet


class TextureType(ABC):
    """
    Représente un type de texture
    """

    loaded_image: dict[Path, pyglet.image.AbstractImage] = {}  # Cache des textures

    @classmethod
    def get_texture(cls, path: Path) -> pyglet.image.AbstractImage:
        """
        Retourne la texture correspondant au chemin donné
        :param path: chemin de la texture
        :return: la texture
        """

        # si la texture n'est pas encore chargée, charge-la
        if (texture := cls.loaded_image.get(path)) is None:
            texture = pyglet.image.load(path)
            cls.loaded_image[path] = texture

        return texture

    @abstractmethod
    def __get__(self, instance, owner) -> pyglet.image.AbstractImage:
        pass
