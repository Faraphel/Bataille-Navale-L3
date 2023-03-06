from pathlib import Path
from typing import TYPE_CHECKING

from source.gui import widget
from source.gui.scene.abc import Scene


if TYPE_CHECKING:
    from source.gui.window import Window


class HistoryGame(Scene):
    def __init__(self, window: "Window", history_path: Path, **kwargs):
        super().__init__(window, **kwargs)

        self.history_path = history_path

        self.add_widget(
            widget.Text,

            x=0.5, y=0.5,

            anchor_x="center", anchor_y="center",

            text=str(history_path)
        )
