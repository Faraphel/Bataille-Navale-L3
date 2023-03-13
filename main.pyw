from pathlib import Path

import pyglet

from source.gui.scene import MainMenu
from source.gui.window import GameWindow


from source.path import path_font
from source.gui.better_pyglet import Label


# Change la police par défaut utilisé pour le Century Gothic
pyglet.font.add_directory(path_font)
Label.default_kwargs["font_name"] = "Century Gothic"  # NOQA: Label à un "default_kwargs" avec la metaclass

# Créer une nouvelle fenêtre
window = GameWindow(
    resizable=True,
    caption="Bataille Navale",
    option_path=Path("./option.json")
)

try: window.set_icon(pyglet.image.load("./assets/image/icon/icon.png"))
except: pass  # NOQA E722

window.set_minimum_size(720, 480)
window.add_scene(MainMenu)

# Démarre la boucle d'événement
pyglet.app.run()
