from pathlib import Path

import pyglet

from source.gui.scene import MainMenu
from source.gui.window import GameWindow


from source.path import path_font, path_image
from source.gui.better_pyglet import Label


# Change le driver audio par défaut
pyglet.options["audio"] = (
    'openal',  # privilégie OpenAL pour le cross platform et moins de problème
    'xaudio2',
    'directsound',
    # 'pulse', # ne propose pas pulse qui a des problèmes de crash
    'silent'
)


# Change la police par défaut utilisé pour le Century Gothic
pyglet.font.add_directory(path_font)
Label.default_kwargs["font_name"] = "Century Gothic"

# Créer une nouvelle fenêtre
window = GameWindow(
    resizable=True,
    caption="Bataille Navale",
    option_path=Path("./option.json")
)

# Change l'icône de cette fenêtre
try: window.set_icon(pyglet.image.load(path_image / "/icon/icon.png"))
except: pass  # NOQA E722

window.set_minimum_size(720, 480)
window.add_scene(MainMenu)

# Démarre la boucle d'événement
pyglet.app.run()
