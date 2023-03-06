from abc import ABC
from typing import Any


class Element(ABC):
    def __init_subclass__(cls, **kwargs):
        cls.default_kwargs: dict[str, Any] = {}  # all subclasses will have their own "default_kwargs" dict
