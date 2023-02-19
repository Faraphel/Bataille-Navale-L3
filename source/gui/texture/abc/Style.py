from abc import ABC
from typing import Optional, Any

import pyglet


class Style(ABC):
    def __init_subclass__(cls, **kwargs):
        atlas = pyglet.image.atlas.TextureAtlas()

        for name, path in cls.__dict__.items():
            if name.startswith("_"): continue
            setattr(cls, name, atlas.add(pyglet.image.load(path)))

        setattr(cls, "_atlas", atlas)

    @classmethod
    def get(cls, item: str, default: Any = None) -> Optional[pyglet.image.AbstractImage]:
        return getattr(cls, item, default)

    def __class_getitem__(cls, item: str) -> Optional[pyglet.image.AbstractImage]:
        return cls.get(item)
