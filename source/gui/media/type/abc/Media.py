from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import pyglet


if TYPE_CHECKING:
    from source.gui.media.abc import MediaGroup


class Media(ABC):
    loaded_media: dict[Path, pyglet.media.Source] = {}

    @classmethod
    def get_media(cls, path: Path, owner: "MediaGroup") -> pyglet.media.Source:
        if (media := cls.loaded_media.get(path)) is None:
            # charge le son
            media = pyglet.media.load(path)
            cls.loaded_media[path] = media

            # modifie la fonction pour jouer le son en utilisant le player
            def _play(loop: bool = False):
                owner.player.next_source()  # passe à la prochaine musique
                owner.player.queue(media)  # ajoute la musique à la queue
                owner.player.play()  # joue la musique
                owner.player.on_eos = (lambda: _play(loop=True)) if loop else (lambda: "pass")

            media.play = _play

            def _play_safe(*args, **kwargs):
                if owner.player.source is media: return
                media.play(*args, **kwargs)  # NOQA

            media.play_safe = _play_safe

        return media

    @abstractmethod
    def __get__(self, instance, owner) -> pyglet.media.Source:
        pass
