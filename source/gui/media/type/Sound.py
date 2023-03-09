from pathlib import Path
from typing import TYPE_CHECKING

import pyglet

from source.gui.media.type.abc import Media


if TYPE_CHECKING:
    from source.gui.media.abc import MediaGroup


class Sound(Media):
    def __init__(self, path: Path):
        self.path = path

    def __get__(self, instance, owner: "MediaGroup") -> pyglet.media.Source:
        return self.get_media(self.path, owner)
