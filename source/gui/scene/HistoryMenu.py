from typing import TYPE_CHECKING

from source import path_history
from source.gui import widget, texture
from source.gui.scene.abc import Scene


if TYPE_CHECKING:
    from source.gui.window import Window


class HistoryMenu(Scene):
    PAGE_SIZE: int = 10

    def __init__(self, window: "Window", page: int = 0, **kwargs):
        super().__init__(window, **kwargs)

        for i, path in enumerate(
            list(path_history.iterdir())
            [page*self.PAGE_SIZE:(page+1)*self.PAGE_SIZE]
        ):

            button = self.add_widget(
                widget.Button,

                x=0.2, y=1.0 - ((i+1) * 0.1), width=0.6, height=0.1,

                label_text=path.stem,

                style=texture.Button.Style1
            )
