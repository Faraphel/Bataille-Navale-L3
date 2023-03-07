from .Value import Value
from .Unit import Unit

px = Unit(lambda value: (lambda widget: value))  # PiXel
vw = Unit(lambda value: (lambda widget: int(widget.scene.window.width * (value / 100))))  # Viewport Width
vh = Unit(lambda value: (lambda widget: int(widget.scene.window.height * (value / 100))))   # Viewport Height
ww = Unit(lambda value: (lambda widget: int(widget.width * (value / 100))))  # Widget Width
wh = Unit(lambda value: (lambda widget: int(widget.height * (value / 100))))  # Widget Height


vw_full, vh_full = 100*vw, 100*vh
vw_center, vh_center = 50*vw, 50*vh

ww_full, wh_full = 100*ww, 100*wh
ww_center, wh_center = 50*ww, 50*wh


def real_right(value: Value) -> Value:  # positionne depuis la droite avec la taille du widget compris
    return vw_full - value


def real_top(value: Value) -> Value:  # positionne depuis le haut avec la taille du widget compris
    return vh_full - value


def right(value: Value) -> Value:  # positionne depuis la droite
    return real_right(value) - ww_full


def top(value: Value) -> Value:  # positionne depuis le haut
    return real_top(value) - wh_full
