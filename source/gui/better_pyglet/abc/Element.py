from abc import ABC
from typing import Any


class Element(ABC):
    default_kwargs: dict[str, Any]

    def __init_subclass__(cls, **kwargs):
        cls.default_kwargs = {}  # all subclasses will have their own "default_kwargs" dict
