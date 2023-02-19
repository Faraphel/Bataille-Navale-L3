from abc import abstractmethod
from functools import lru_cache
from typing import Callable, Any

from source.gui.event import StopEvent


class EventPropagationMixin:
    @property
    @abstractmethod
    def childs(self):
        pass

    @lru_cache
    def _event_wrapper(self, item: str) -> Callable:
        """
        Un wrapper permettant d'appeler l'événement de toutes les scènes attachées.
        :param item: nom de la fonction à appeler dans la scène.
        :return: une fonction appelant l'événement original ainsi que ceux des scènes.
        """

        # if the event is the drawing of the objects, reverse the order of the scenes
        # so that the last drawn are the one on top
        child_transform = (
            (lambda child: reversed(child)) if item == "on_draw" else
            (lambda child: child)
        )

        # try to get the original function
        func = None
        try: func = super().__getattribute__(item)
        except AttributeError: pass

        # try to get a function that would get executed after everything else
        func_after = None
        try: func_after = super().__getattribute__(item + "_after")
        except AttributeError: pass

        def _func(*args, **kwargs) -> None:
            if func is not None: func(*args, **kwargs)

            for child in child_transform(self.childs):
                try: getattr(child, item, lambda *_, **__: "pass")(*args, **kwargs)
                # si l'erreur StopEventScene est détecté, les autres scènes ne recevront pas l'event
                except StopEvent: break

            if func_after is not None: func_after(*args, **kwargs)

        return _func

    def __getattribute__(self, item: str) -> Any:
        """
        Fonction appelée dès que l'on essaye d'accéder à l'un des attributs de l'objet.
        :param item: nom de l'attribut recherché
        :return: l'attribut de l'objet correspondant.
        """

        # si l'attribut est un événement (commence par "on_"), alors renvoie le dans un wrapper
        return self._event_wrapper(item) if item.startswith("on_") else super().__getattribute__(item)
