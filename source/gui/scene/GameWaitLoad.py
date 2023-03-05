from pathlib import Path
from typing import TYPE_CHECKING

from source.gui import widget
from source.gui.scene.abc import Scene
from source.utils import path_ctime_str

if TYPE_CHECKING:
    from source.gui.window import Window


class GameWaitLoad(Scene):
    def __init__(self, window: "Window", path: Path, **kwargs):
        super().__init__(window, **kwargs)

        self.label = self.add_widget(
            widget.Text,

            x=0.5, y=0.5, width=1.0,

            anchor_x="center",

            text=f"Une ancienne sauvegarde à été trouvé.\n"
                 f"L'hôte décide de son utilisation...\n"
                 f"({path_ctime_str(path)})",

            align="center",
            multiline=True,
            font_size=28,
        )
