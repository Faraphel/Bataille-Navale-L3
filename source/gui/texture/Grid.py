from .abc import Style
from .type import Texture, Animation
from source.path import path_image

path = path_image / "grid"
path_boat = path / "boat"


class Grid:
    class Style1(Style):
        background = Texture(path / "background.png")

    class Boat:
        class Style1(Style):
            _animation = sorted(
                (path_boat / "animation").iterdir(),
                key=lambda path: int(path.stem)
            )

            body = Texture(path_boat / "body.png")
            edge = Texture(path_boat / "edge.png")
            solo = Texture(path_boat / "solo.png")

            missed = Animation([*_animation, path_boat / "missed.png"], 0.03, False)
            touched = Animation([*_animation, path_boat / "touched.png"], 0.03, False)
