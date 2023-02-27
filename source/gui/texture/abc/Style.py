from abc import ABC
from pathlib import Path
from typing import Optional, Any

import pyglet


class Style(ABC):
    """
    This class represent a style that can be attached to a widget.
    """

    @classmethod
    def __getattr__(cls, item):
        return None  # by default, an object will be None if not found.

    @classmethod
    def get(cls, item, default=None):
        return getattr(cls, item, default)
