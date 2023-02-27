from . import path
from .abc import Style
from .type import Texture, Animation

path = path / "grid"
path_boat = path / "boat"
path_bomb = path / "bomb"


class Grid:
    class Style1(Style):
        background = Texture(path / "background.png")

    class Boat:
        class Style1(Style):
            body = Texture(path_boat / "body.png")
            edge = Texture(path_boat / "edge.png")
            solo = Texture(path_boat / "solo.png")

    class Bomb:
        class Style1(Style):
            _animation = sorted(
                (path_bomb / "animation").iterdir(),
                key=lambda path: int(path.stem)
            )

            missed = Animation([*_animation, path_bomb / "missed.png"], 0.03, False)
            touched = Animation([*_animation, path_bomb / "touched.png"], 0.03, False)
