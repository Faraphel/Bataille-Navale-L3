from abc import ABC
from functools import lru_cache
from typing import TYPE_CHECKING, Callable, Type, Any

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.widget.abc import Widget


class Scene(ABC):
    """
    A scene that can be attached to a window.
    It allows to switch the whole comportment of the window in a simpler way.

    It can react to any "on_" event from the window.
    """

    def __init__(self, window: "Window", *args, **kwargs):
        self.window = window
        self._widgets: set["Widget"] = set()

    # Widget Managing

    def add_widget(self, widget_class: Type["Widget"], **widget_kwargs):
        """
        Add a widget to the scene.
        :widget_class: the class of the widget to add.
        :widget_args: args for the creation of the widget object.
        :widget_kwargs: kwargs for the creation of the widget object.
        :return: the new created widget.
        """

        widget: "Widget" = widget_class(self, **widget_kwargs)
        self._widgets.add(widget)
        return widget

    def remove_widget(self, widget: "Widget") -> None:
        """
        Remove a widget from the scene.
        :scene: the widget to remove.
        """

        self._widgets.remove(widget)

    def clear_widget(self) -> None:
        """
        Clear the scene from all the widgets.
        """

        self._widgets.clear()

    # Event Handling

    @lru_cache
    def _event_wrapper(self, item: str) -> Callable:
        """
        Un wrapper permettant d'appeler l'événement de tous les widgets attachées.
        :param item: nom de la fonction à appeler dans le widget.
        :return: une fonction appelant l'événement original ainsi que ceux des scènes.
        """

        # Récupère la fonction originale. S'il n'y en a pas, renvoie une fonction sans effet.*
        func = None
        try: func = super().__getattribute__(item)
        except AttributeError: pass

        def _func(*args, **kwargs) -> None:
            if func is not None: func(*args, **kwargs)
            for widget in self._widgets:
                getattr(widget, item, lambda *_, **__: "pass")(*args, **kwargs)

        return _func

    def __getattribute__(self, item: str) -> Any:
        """
        Fonction appelée dès que l'on essaye d'accéder à l'un des attributs de l'objet.
        :param item: nom de l'attribut recherché
        :return: l'attribut de l'objet correspondant.
        """

        # si l'attribut est un événement (commence par "on_"), alors renvoie le dans un wrapper
        return self._event_wrapper(item) if item.startswith("on_") else super().__getattribute__(item)
