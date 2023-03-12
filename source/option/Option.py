import json
from pathlib import Path
from typing import TYPE_CHECKING

from source.gui import media

if TYPE_CHECKING:
    from source.gui.window import GameWindow


class Option:
    def __init__(self, window: "GameWindow",
                 volume_ambient: float = 0.1,
                 volume_fx: float = 0.1,
                 fps_show: bool = False,
                 fps_limit: int = 60,
                 vsync: bool = True
                 ):
        self.window = window
        self.volume_ambient = volume_ambient
        self.volume_fx = volume_fx
        self.fps_show = fps_show
        self.fps_limit = fps_limit
        self.vsync = vsync

    # propriété

    @property
    def volume_ambient(self) -> float:
        return media.SoundAmbient.get_volume()

    @volume_ambient.setter
    def volume_ambient(self, value: float):
        media.SoundAmbient.set_volume(value)

    @property
    def volume_fx(self) -> float:
        return media.SoundEffect.get_volume()

    @volume_fx.setter
    def volume_fx(self, value: float):
        media.SoundEffect.set_volume(value)

    @property
    def fps_show(self):
        return self.window.fps_enable

    @fps_show.setter
    def fps_show(self, value: bool):
        self.window.set_fps_enabled(value)

    @property
    def fps_limit(self):
        return self.window.get_fps()

    @fps_limit.setter
    def fps_limit(self, value: float):
        self.window.set_fps(value)

    @property
    def vsync(self):
        return self.window.vsync

    @vsync.setter
    def vsync(self, value: bool):
        self.window.set_vsync(value)

    # chargement et sauvegarde

    def to_json(self) -> dict:
        return {
            "volume_ambient": self.volume_ambient,
            "volume_fx": self.volume_fx,
            "fps_show": self.fps_show,
            "fps_limit": self.fps_limit,
            "vsync": self.vsync,
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
