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
    A scene that can be attached to a window.
    It allows to switch the whole comportment of the window in a simpler way.

    It can react to any "on_" event from the window.
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
        Add a widget to the scene.
        :param widget_class: the class of the widget to add.
        :param priority: the priority of the widget.
        :param widget_kwargs: kwargs for the creation of the widget object.
        :return: the new created widget.
        """

        widget: "Widget" = widget_class(self, **widget_kwargs)
        self._widgets.insert(priority, widget)
        return widget

    def remove_widget(self, widget: "Widget") -> None:
        """
        Remove a widget from the scene.
        :param widget: the widget to remove.
        """

        self._widgets.remove(widget)

    def clear_widget(self) -> None:
        """
        Clear the scene from all the widgets.
        """

        self._widgets.clear()

    # shortcut

    @property
    def valid(self) -> bool:
        """
        Indique si la scène à tout ses éléments de formulaire valides
        :return: True si tous les éléments (Input, ...) sont correctement rempli.
        """

        for widget in self._widgets:
            if isinstance(widget, Input) and widget.invalid: return False

        return True

    # event

    def on_draw(self) -> None:
        """
        Draw all the objects in the scene.
        """

        self.batch.draw()
