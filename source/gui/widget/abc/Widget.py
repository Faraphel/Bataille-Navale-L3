from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Widget(ABC):
    """
    A Widget that can be attached to a scene.

    It can react to any "on_" event from the scene.
    """

    def __init__(self, scene: "Scene", *args, **kwargs):
        self.scene = scene
