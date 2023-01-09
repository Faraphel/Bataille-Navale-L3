from source.gui.scene.base import Scene
from source.gui.widget.Button import Button

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.gui.window import Window


class MainMenuScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_widget(Button())

    def on_draw(self, window: "Window"):
        super().on_draw(window)

