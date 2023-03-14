from abc import ABC
from typing import TYPE_CHECKING, Optional

from source.gui.widget.abc import Widget
from source.type import Distance, Point2D
from source.utils import in_bbox

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class BoxWidget(Widget, ABC):
    """
    Pareil qu'un Widget, mais dans une boîte de collision (bbox)
    """

    def __init__(self, scene: "Scene",
                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None):
        super().__init__(scene)

        # Défini les bordures de la boîte de collision. Peut utiliser des nombres ou des unités de distance
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.hovering = False  # La bbox est-elle actuellement survolée ?
        self.clicking = False  # La bbox est-elle actuellement cliqué ?
        self.activated = False  # La bbox est-il actuellement activé ? (le dernier clic a été à l'intérieur)

    # propriétés

    def _getter_distance(self, raw_distance: Distance) -> int:
        """
        Renvoie la distance en pixel d'une distance abstraite
        :param raw_distance: la distance à convertir en pixel
        :return: la vrai distance en pixel
        """

        if isinstance(raw_distance, int): return raw_distance
        if callable(raw_distance): return raw_distance(self)
        if raw_distance is None: return 0

        raise TypeError(f"Invalid type for the distance : {type(raw_distance)}")

    @property
    def x(self) -> int: return self._getter_distance(self._x)

    @x.setter
    def x(self, x: Distance):  self._x = x

    @property
    def y(self) -> int: return self._getter_distance(self._y)

    @y.setter
    def y(self, y: Distance): self._y = y

    @property
    def xy(self) -> tuple[int, int]: return self.x, self.y

    @property
    def x2(self) -> int: return self.x + self.width

    @property
    def y2(self) -> int: return self.y + self.height

    @property
    def xy2(self) -> tuple[int, int]: return self.x2, self.y2

    @property
    def width(self) -> int: return self._getter_distance(self._width)

    @width.setter
    def width(self, width: Optional[Distance]): self._width = width

    @property
    def height(self) -> int: return self._getter_distance(self._height)

    @height.setter
    def height(self, height: Optional[Distance]): self._height = height

    @property
    def size(self) -> tuple[int, int]: return self.width, self.height

    @property
    def bbox(self) -> tuple[int, int, int, int]: return self.x, self.y, self.x2, self.y2

    @property
    def center_x(self) -> float: return self.x + (self.width / 2)

    @property
    def center_y(self) -> float: return self.y + (self.height / 2)

    @property
    def center(self) -> tuple[float, float]: return self.center_x, self.center_y

    # fonctions

    def in_bbox(self, point: Point2D) -> bool:
        return in_bbox(point, self.bbox)

    # événements

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """
        Lorsque la souris est déplacée, cet événement est déclenché.
        Permet d'implémenter les événements on_hover, on_hover_enter et on_hover_leave
        :param x: la position x de la souris
        :param y: la position y de la souris
        :param dx: la différence de la position x de la souris
        :param dy: la différence de la position y de la souris
        """

        rel_x, rel_y = x - self.x, y - self.y

        old_hovering = self.hovering
        self.hovering = self.in_bbox((x, y))

        if old_hovering != self.hovering:  # si le survole a changé d'état
            # appelle d'événement on_hover_change
            self.trigger_event("on_hover_change", rel_x, rel_y)
            # appelle l'événement on_hover_enter ou on_hover_leave selon la valeur
            self.trigger_event("on_hover_enter" if self.hovering else "on_hover_leave", rel_x, rel_y)

        if self.hovering:  # si la souris est dans la bbox actuellement
            self.trigger_event("on_hover", rel_x, rel_y)  # appelle l'événement on_hover

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """
        Lorsque la souris est cliqué, cet événement est déclenché.
        :param x: la position x de la souris
        :param y: la position y de la souris
        :param button: button de la souris cliqué
        :param modifiers: modificateur du bouton de la souris
        """

        rel_x, rel_y = x - self.x, y - self.y

        self.activated = self.in_bbox((x, y))
        self.trigger_event("on_activate_change", rel_x, rel_y, button, modifiers)

        if self.activated:  # si le clic s'est produit dans la bbox
            # appel des événements on_activate_enter
            self.trigger_event("on_activate_enter", rel_x, rel_y, button, modifiers)

            self.clicking = True  # défini le widget comme étant à présent cliqué
            # appel des événements on_click_change et on_click_press
            self.trigger_event("on_click_change", rel_x, rel_y, button, modifiers)
            self.trigger_event("on_click_press", rel_x, rel_y, button, modifiers)

        else:
            # si le clic n'était pas dans la bbox, appel de l'événement on_activate_leave
            self.trigger_event("on_activate_leave", rel_x, rel_y, button, modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        """
        Lorsque le clic de la souris est relâché, cet événement est déclenché.
        :param x: la position x de la souris
        :param y: la position y de la souris
        :param button: button de la souris cliqué
        :param modifiers: modificateur du bouton de la souris
        """

        rel_x, rel_y = x - self.x, y - self.y

        old_click: bool = self.clicking
        self.clicking = False  # le widget n'est plus cliqué

        if not self.in_bbox((x, y)): return  # si le clic n'a pas été relâché dans la bbox, ignore

        if old_click:  # si ce bouton était celui qui était survolé lorsque le bouton a été cliqué
            # déclenche les événements on_click_change et on_click_release
            self.trigger_event("on_click_change", rel_x, rel_y, button, modifiers)
            self.trigger_event("on_click_release", rel_x, rel_y, button, modifiers)
