from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.scene.abc import Scene
from source.network import Host

if TYPE_CHECKING:
    from source.gui.window import Window


class GameWaitLoad(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.label = self.add_widget(
            widget.Text,

            x=0.5, y=0.5, width=1.0,

            anchor_x="center",

            text="Une ancienne sauvegarde à été trouvé.\nL'hôte décide de son utilisation...",
            align="center",
            multiline=True,
            font_size=28,
        )
