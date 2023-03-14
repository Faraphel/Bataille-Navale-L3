from abc import abstractmethod
from functools import lru_cache
from typing import Callable, Any

from source.gui.event import StopEvent


class EventPropagationMixin:
    """
    Les classes héritant de cette classe peuvent propager tous les appels des méthodes qui commençent par "on_" aux
    objets présents dans la propriété "childs"
    """

    @property
    @abstractmethod
    def childs(self) -> list:
        """
        Renvoie la liste des objets auquel propagé les événements
        :return: la liste des objets auquel propagé les événements
        """
        pass

    @lru_cache
    def _event_wrapper(self, item: str) -> Callable:
        """
        Un wrapper permettant d'appeler l'événement de toutes les scènes attachées.
        :param item: nom de la fonction à appeler dans la scène.
        :return: une fonction appelant l'événement original ainsi que ceux des scènes.
        """

        # Si l'événement est à propos de dessiner les objets,
        # inverse l'ordre pour que les derniers objets dessinés soit au-dessus des autres.
        child_transform = (
            (lambda child: reversed(child)) if item == "on_draw" else
            (lambda child: child)
        )

        # essaye de récupérer la fonction originale
        func = None
        try: func = super().__getattribute__(item)
        except AttributeError: pass

        # essaye de récupérer une fonction qui devrait s'exécuter après les autres
        func_after = None
        try: func_after = super().__getattribute__(item + "_after")
        except AttributeError: pass

        def _func(*args, **kwargs) -> None:
            if func is not None: func(*args, **kwargs)

            for child in child_transform(self.childs):
                try: getattr(child, item, lambda *_, **__: "pass")(*args, **kwargs)
                # si l'erreur StopEventScene est détecté, les autres scènes ne recevront pas l'événement
                except StopEvent: break

            if func_after is not None: func_after(*args, **kwargs)

        return _func

    def __getattribute__(self, item: str) -> Any:
        """
        Fonction appelée dès que l'on essaye d'accéder à l'un des attributs de l'objet
        :param item: nom de l'attribut recherché
        :return: l'attribut de l'objet correspondant
        """

        # si l'attribut est un événement (commence par "on_"), alors renvoie le dans un wrapper
        return self._event_wrapper(item) if item.startswith("on_") else super().__getattribute__(item)
