from pathlib import Path
from typing import TYPE_CHECKING

from source.gui import widget, texture, media
from source.gui.position import vw_full, vh, vw, vh_full
from source.gui.scene.abc import Scene
from source.utils import path_ctime_str

if TYPE_CHECKING:
    from source.gui.window import Window


class GameWaitLoad(Scene):
    """
    Cette scène sert de salle d'attente pour le client qui attend de charger ou non sa sauvegarde
    """

    def __init__(self, window: "Window", path: Path, **kwargs):
        super().__init__(window, **kwargs)

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=vw_full, height=vh_full,

            image=texture.Background.choice
        )

        self.label = self.add_widget(
            widget.Text,

            x=50*vw, y=50*vh, width=vw_full,

            anchor_x="center",

            text=f"Une ancienne sauvegarde à été trouvé.\n"
                 f"L'hôte décide de son utilisation...\n"
                 f"({path_ctime_str(path)})",

            align="center",
            multiline=True,
            font_size=28,
        )

        media.SoundAmbient.menu.play_safe(loop=True)
