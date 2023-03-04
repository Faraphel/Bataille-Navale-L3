from abc import ABC


class SoundGroup(ABC):
    """
    This class represent a music group that can be played.
    """

    @classmethod
    def get(cls, item, default=None):
        return getattr(cls, item, default)
