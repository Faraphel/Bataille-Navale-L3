from abc import ABC


class Style(ABC):
    """
    This class represent a style that can be attached to a widget.
    """

    @classmethod
    def get(cls, item, default=None):
        return getattr(cls, item, default)
