from .type import Sound
from .abc import MediaGroup
from source.path import path_sound

path = path_sound / "game"


class Game(MediaGroup):
    touched = Sound(path / "touched.wav")
    sunken_ally = Sound(path / "sunken_ally.wav")
    won = Sound(path / "won.wav")

    missed = Sound(path / "missed.wav")
    sunken_enemy = Sound(path / "sunken_enemy.wav")
    loose = Sound(path / "loose.wav")
