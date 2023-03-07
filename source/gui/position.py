from typing import Callable


# pourcentage


def w_percent(value: float) -> Callable:  # positionne en pourcentage la largeur
    return lambda widget: int(widget.scene.window.width * (value / 100))


def h_percent(value: float) -> Callable:  # positionne en pourcentage la hauteur
    return lambda widget: int(widget.scene.window.height * (value / 100))


# pixel


def right(px: int) -> Callable:  # positionne depuis la droite
    return lambda widget: widget.scene.window.width - px


def up(px: int) -> Callable:  # positionne depuis le haut
    return lambda widget: widget.scene.window.height - px


def right_content(px: int) -> Callable:  # positionne depuis la droite avec la taille du widget compris
    return lambda widget: widget.scene.window.width - widget.width - px


def up_content(px: int) -> Callable:  # positionne depuis le haut avec la taille du widget compris
    return lambda widget: widget.scene.window.height - widget.height - px


# raccourci

w_full = w_percent(100)
h_full = h_percent(100)
