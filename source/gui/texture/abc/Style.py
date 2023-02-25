from abc import ABC
from pathlib import Path
from typing import Optional, Any

import pyglet


class Style(ABC):
    """
    This class represent a style that can be attached to a widget.
    All property of the class will be loaded into a pyglet image.

    If the property is associated to only a Path, a simple image will be loaded.
    If the property is associated to a list of Path, an animation will be loaded.
    """

    def __init_subclass__(cls, **kwargs):
        for name, args in cls.__dict__.items():
            if name.startswith("_"): continue

            if isinstance(args, Path):  # if this is a normal path for a normal image
                path = args
                texture = pyglet.image.load(path)

            elif isinstance(args, tuple) and len(args) == 3:  # if this is a tuple for an animation
                paths, duration, loop = args
                textures = map(pyglet.image.load, paths)
                texture = pyglet.image.Animation.from_image_sequence(textures, duration, loop)

            else:
                raise ValueError(f"Invalid type : {type(args)}")

            setattr(cls, name, texture)

    @classmethod
    def get(cls, item: str, default: Any = None) -> Optional[pyglet.image.AbstractImage]:
        return getattr(cls, item, default)

    def __class_getitem__(cls, item: str) -> Optional[pyglet.image.AbstractImage]:
        return cls.get(item)
