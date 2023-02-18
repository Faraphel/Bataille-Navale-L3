from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from source.event import Listener

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Widget(Listener, ABC):
    """
    A Widget that can be attached to a scene.

    It can react to any "on_" event from the scene.
    """

    def __init__(self, scene: "Scene", **kwargs):
        super().__init__()

        self.scene = scene

    @abstractmethod
    def draw(self):
        """
        The draw function. Can be called to draw the widget.
        """
