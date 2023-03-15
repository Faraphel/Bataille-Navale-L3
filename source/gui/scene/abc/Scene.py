from abc import ABC
from typing import TYPE_CHECKING, Type

import pyglet

from source.gui.event import EventPropagationMixin
from source.gui.widget import Input

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.widget.abc import Widget


class Scene(ABC, EventPropagationMixin):
    """
    Une scène pouvant être attaché à une fenêtre.
    Permet de changer le comportement entier et les widgets de la fenêtre plus simplement.

    Il peut réagir à n'importe quel événement de pyglet d'une fenêtre.
    """

    def __init__(self, window: "Window", **kwargs):
        self.window = window

        self.batch = pyglet.graphics.Batch()
        self._widgets: list["Widget"] = list()

    # Event propagation

    @property
    def childs(self):
        return self._widgets

    # Widget Managing

    def add_widget(self, widget_class: Type["Widget"], priority: int = 0, **widget_kwargs):
        """
        Ajoute un widget à la scène
        :param widget_class: La classe du widget à ajouter
        :param priority: la priorité du widget (force un widget à apparaître au-dessus des autres)
        :param widget_kwargs: les arguments clé de la création du widget
        :return: le widget créé
        """

        widget: "Widget" = widget_class(self, **widget_kwargs)
        self._widgets.insert(priority, widget)
        return widget

    def remove_widget(self, widget: "Widget") -> None:
        """
        Retire un widget de la scène
        :param widget: le widget à retirer
        """

        self._widgets.remove(widget)

    def clear_widget(self) -> None:
        """
        Supprime de la scène tous les widgets
        """

        self._widgets.clear()

    # shortcut

    @property
    def valid(self) -> bool:
        """
        Indique si la scène à tous ses éléments de formulaire valides
        :return: True si tous les éléments (Input, ...) sont correctement rempli.
        """

        for widget in self._widgets:
            if isinstance(widget, Input) and not widget.valid: return False

        return True

    # event

    def on_draw(self) -> None:
        """
        Dessines tous les objets de la scène
        """

        self.batch.draw()
