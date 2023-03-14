from abc import ABC

import pyglet


class MediaGroup(ABC):
    """
    Cette classe représente un groupe de musique pouvant être joué.
    """

    player: pyglet.media.Player

    def __init_subclass__(cls, **kwargs):
        cls.player = pyglet.media.Player()

    @classmethod
    def get(cls, item, default=None):
        return getattr(cls, item, default)

    @classmethod
    def get_volume(cls):
        return cls.player.volume

    @classmethod
    def set_volume(cls, value: float):
        cls.player.volume = value

    @classmethod
    def stop(cls):
        cls.player.next_source()
