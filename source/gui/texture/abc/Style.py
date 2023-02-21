from abc import ABC
from pathlib import Path
from typing import Optional, Any

import pyglet


class Style(ABC):
    def __init_subclass__(cls, **kwargs):
        atlas = pyglet.image.atlas.TextureAtlas()

        for name, args in cls.__dict__.items():
            if name.startswith("_"): continue

            if isinstance(args, Path):  # if this is a normal path for a normal image
                path = args
                texture = atlas.add(pyglet.image.load(path))

            elif isinstance(args, tuple):  # if this is a tuple for an animation
                paths, duration, loop = args

                textures = map(lambda path: atlas.add(pyglet.image.load(path)), paths)
                texture = pyglet.image.Animation.from_image_sequence(textures, duration, loop)

            else:
                raise ValueError(f"Invalid type : {type(args)}")

            setattr(cls, name, texture)

        setattr(cls, "_atlas", atlas)

    @classmethod
    def get(cls, item: str, default: Any = None) -> Optional[pyglet.image.AbstractImage]:
        return getattr(cls, item, default)

    def __class_getitem__(cls, item: str) -> Optional[pyglet.image.AbstractImage]:
        return cls.get(item)
