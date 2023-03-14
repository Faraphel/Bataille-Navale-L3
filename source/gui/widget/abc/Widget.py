from abc import ABC
from typing import TYPE_CHECKING

from source.event import Listener

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Widget(Listener, ABC):
    """
    Un widget pouvant être attaché à une scène.

    Il peut réagir à n'importe quel événement "on_" de la scène.
    """

    def __init__(self, scene: "Scene", **kwargs):
        super().__init__()

        self.scene = scene
