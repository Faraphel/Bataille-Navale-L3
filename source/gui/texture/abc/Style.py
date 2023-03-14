from abc import ABC


class Style(ABC):
    """
    Cette classe représente un style pouvant être appliqué sur un widget.
    """

    @classmethod
    def get(cls, item, default=None):
        return getattr(cls, item, default)
