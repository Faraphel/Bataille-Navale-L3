from .type import Sound
from .abc import MediaGroup
from source.path import path_sound

path = path_sound / "effect"


class SoundEffect(MediaGroup):
    placed = Sound(path / "placed.wav")
    touched = Sound(path / "touched.wav")
    missed = Sound(path / "missed.wav")
    sunken = Sound(path / "sunken.wav")
    victory = Sound(path / "victory.wav")
    defeat = Sound(path / "defeat.wav")
