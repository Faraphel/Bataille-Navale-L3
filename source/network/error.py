import builtins
from typing import TYPE_CHECKING

from source.utils.thread import in_pyglet_context


if TYPE_CHECKING:
    from source.gui.window import Window


def handle_error(window: "Window", exception: Exception):
    """
    Fonction permettant d'afficher le bon message d'erreur du au réseau.
    :param window: la fenêtre du jeu
    :param exception: l'erreur qui s'est produite
    """

    message: str = "Erreur :\n"

    # récupère le message d'erreur selon le type de l'erreur
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
