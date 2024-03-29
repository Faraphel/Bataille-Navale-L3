from .abc import MediaGroup
from source.path import path_sound
from .type import Sound

path = path_sound / "ambient"


class SoundAmbient(MediaGroup):
    """
    Groupe contenant les sons ambient du jeu.
    """

    menu = Sound(path / "menu.wav")
    sea = Sound(path / "sea.wav")
