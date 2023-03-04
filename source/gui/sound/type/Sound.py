from pathlib import Path

import pyglet

from source.gui.sound.type.abc import SoundType


class Sound(SoundType):
    def __init__(self, path: Path):
        self.path = path

    def __get__(self, instance, owner) -> pyglet.media.Source:
        return self.get_sound(self.path)
