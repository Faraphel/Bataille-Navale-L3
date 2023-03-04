from abc import ABC, abstractmethod
from pathlib import Path

import pyglet


class SoundType(ABC):
    loaded_sound: dict[Path, pyglet.media.Source] = {}

    @classmethod
    def get_sound(cls, path: Path) -> pyglet.media.Source:
        if (sound := cls.loaded_sound.get(path)) is None:
            sound = pyglet.media.load(path)
            cls.loaded_sound[path] = sound

        return sound

    @abstractmethod
    def __get__(self, instance, owner) -> pyglet.image.AbstractImage:
        pass
