from . import path
from .abc import Style

path = path / "grid"
path_boat = path / "boat"
path_bomb = path / "bomb"


class Grid:
    class Style1(Style):
        background = path / "background.png"

    class Boat:
        class Style1(Style):
            body = path_boat / "body.png"
            edge = path_boat / "edge.png"
            broken = path_boat / "broken.png"
            solo = path_boat / "solo.png"

    class Bomb:
        class Style1(Style):
            _animation = sorted(
                    (path_bomb / "animation").iterdir(),
                    key=lambda path: int(path.stem)
            )

            missed = [*_animation, path_bomb / "missed.png"], 0.03, False
            touched = [*_animation, path_bomb / "touched.png"], 0.03, False
