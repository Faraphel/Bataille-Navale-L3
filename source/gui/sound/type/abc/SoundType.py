from abc import ABC, abstractmethod
from pathlib import Path

import pyglet


class SoundType(ABC):
    loaded_sound: dict[Path, pyglet.media.Source] = {}
    player: pyglet.media.Player

    def __init_subclass__(cls, **kwargs):
        cls.player = pyglet.media.Player()

    @classmethod
    def get_sound(cls, path: Path) -> pyglet.media.Source:
        if (sound := cls.loaded_sound.get(path)) is None:
            # charge le son
            sound = pyglet.media.load(path)
            cls.loaded_sound[path] = sound

            # modifie la fonction pour jouer le son en utilisant le player
            def _play():
                cls.player.delete()  # arrête la musique en cours s'il y en a une et vide la queue
                cls.player.queue(sound)  # ajoute la musique à la queue
                cls.player.play()  # joue la musique

            sound.play = _play

        return sound

    @abstractmethod
    def __get__(self, instance, owner) -> pyglet.image.AbstractImage:
        pass

    @property
    def volume(self):
        return self.player.volume

    @volume.setter
    def volume(self, volume: float):
        self.player.volume = volume
