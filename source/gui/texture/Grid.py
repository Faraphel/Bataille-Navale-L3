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
            _anim_bomb = sorted((path_boat / "anim_bomb").iterdir(), key=lambda path: int(path.stem))
            _anim_body = sorted((path_boat / "anim_body").iterdir(), key=lambda path: int(path.stem))
            _anim_edge = sorted((path_boat / "anim_edge").iterdir(), key=lambda path: int(path.stem))
            _anim_solo = sorted((path_boat / "anim_solo").iterdir(), key=lambda path: int(path.stem))

            body = Animation([*_anim_body, path_boat / "body.png"], 0.03, False)
            edge = Animation([*_anim_edge, path_boat / "edge.png"], 0.03, False)
            solo = Animation([*_anim_solo, path_boat / "solo.png"], 0.03, False)

            preview_body = Texture(path_boat / "preview_body.png")
            preview_edge = Texture(path_boat / "preview_edge.png")
            preview_solo = Texture(path_boat / "preview_solo.png")

            missed = Animation([*_anim_bomb, path_boat / "missed.png"], 0.03, False)
            touched = Animation([*_anim_bomb, path_boat / "touched.png"], 0.03, False)
