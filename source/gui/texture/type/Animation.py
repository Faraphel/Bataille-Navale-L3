from pathlib import Path
from typing import Iterable

import pyglet

from source.gui.texture.type.abc import TextureType


class Animation(TextureType):
    def __init__(self, paths: Iterable[Path], frame_duration: float, loop: bool = True):
        self.paths = paths
        self.frame_duration = frame_duration
        self.loop = loop

    def __get__(self, instance, owner) -> pyglet.image.Animation:
        return pyglet.image.Animation.from_image_sequence(
            sequence=map(self.get_texture, self.paths),
            duration=self.frame_duration,
            loop=self.loop
        )
