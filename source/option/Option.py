import json
from pathlib import Path
from typing import TYPE_CHECKING

from source.gui import media

if TYPE_CHECKING:
    from source.gui.window import GameWindow


class Option:
    """
    Cette classe permet de modifier, sauvegarder et charger les options.
    """

    def __init__(self, window: "GameWindow",
                 volume_ambient: float = 0.1,
                 volume_fx: float = 0.1,
                 fps_show: bool = False,
                 fps_limit: int = 60,
                 vsync: bool = True
                 ):
        self.window = window

        self.set_volume_ambient(volume_ambient)
        self.set_volume_fx(volume_fx)
        self.set_fps_show(fps_show)
        self.set_fps_limit(fps_limit)
        self.set_vsync(vsync)

    # propriétés

    @staticmethod
    def get_volume_ambient() -> float: return media.SoundAmbient.get_volume()
    @staticmethod
    def set_volume_ambient(value: float): media.SoundAmbient.set_volume(value)

    @staticmethod
    def get_volume_fx() -> float: return media.SoundEffect.get_volume()
    @staticmethod
    def set_volume_fx(value: float): media.SoundEffect.set_volume(value)

    def get_fps_show(self): return self.window.fps_enable
    def set_fps_show(self, value: bool): self.window.fps_enable = value

    def get_fps_limit(self): return self.window.get_fps()
    def set_fps_limit(self, value: float): self.window.set_fps(value)

    def get_vsync(self): return self.window.vsync
    def set_vsync(self, value: bool): self.window.set_vsync(value)

    # chargement et sauvegarde

    def to_json(self) -> dict:
        return {
            "volume_ambient": self.get_volume_ambient(),
            "volume_fx": self.get_volume_fx(),
            "fps_show": self.get_fps_show(),
            "fps_limit": self.get_fps_limit(),
            "vsync": self.get_vsync(),
        }

    @classmethod
    def from_json(cls, window: "GameWindow", data: dict) -> "Option":
        return cls(window=window, **data)

    def save(self, path: Path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.to_json(), file)

    @classmethod
    def load(cls, window: "GameWindow", path: Path) -> "Option":
        with open(path, "r", encoding="utf-8") as file:
            return cls.from_json(window=window, data=json.load(file))
