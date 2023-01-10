from source.gui.scene.base import Scene

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.gui.window import Window


class MainMenuScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_draw(self, window: "Window"):
        super().on_draw(window)

