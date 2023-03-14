from pathlib import Path

import pyglet.window

from source.gui.window import Window
from source.option import Option
from source.type import ColorRGBA


class GameWindow(Window):  # NOQA
    """
    Similaire à la classe Window, mais ajoute quelque fonctionnalités pratique pour un jeu. (Option, FPS, etc.)
    """

    def __init__(self,

                 option_path: Path = None,

                 fps_color: ColorRGBA = (255, 255, 255, 200),
                 fps_enable: bool = False,

                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._fps_counter = pyglet.window.FPSDisplay(self, color=fps_color)
        self.fps_enable = fps_enable

        self.option = None
        self.option_path = option_path

        # Créer un événement juste après le debut de la boucle pour charger les options.
        # Puisque pyglet.app.run va limiter les FPS à 60, les options doivent être chargées juste après
        # afin que les anciens paramètres de FPS soient appliqués.
        pyglet.clock.schedule_once(lambda *_: self.load_option(), 0)

    def load_option(self):
        """
        Charge les options depuis le fichier self.option_path.
        """

        try:
            if self.option_path.exists():
                self.option = Option.load(self, self.option_path)
        except Exception:  # NOQA
            pass

        if self.option is None: self.option = Option(window=self)

    def on_draw_after(self):
        # après que tous les éléments ont été dessinés, dessiner le compteur de FPS s'il est activé.
        if self.fps_enable: self._fps_counter.draw()
