from abc import ABC
from typing import Any


class Element(ABC):
    """
    Un mixin pour les éléments de base de pyglet
    """

    default_kwargs: dict[str, Any]

    def __init_subclass__(cls, **kwargs):
        # toutes les sous-classes auront leur propre dictionnaire "default_kwargs"
        cls.default_kwargs = {}
