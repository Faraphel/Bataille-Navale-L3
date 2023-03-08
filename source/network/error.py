import builtins
from typing import TYPE_CHECKING

from source.utils.thread import in_pyglet_context


if TYPE_CHECKING:
    from source.gui.window import Window


def handle_error(window: "Window", exception: Exception):
    message: str = "Erreur :\n"

    match type(exception):
        case builtins.ConnectionResetError:
            message += "Perte de connexion avec l'adversaire."
        case _:
            message += str(exception)

    from source.gui.scene import GameError
    in_pyglet_context(
        window.set_scene,
        GameError,
        text=message
    )
