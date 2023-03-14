import itertools
from math import inf
from typing import Type, TYPE_CHECKING

import pyglet

from source.gui.event import EventPropagationMixin

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Window(pyglet.window.Window, EventPropagationMixin):  # NOQA
    """
    Une fenêtre basée sur l'objet Window de pyglet.
    Des scènes peuvent y être placé.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scenes: list["Scene"] = list()

    # Event Propagation

    @property
    def childs(self):
        """
        Renvoie les scènes de la fenêtre. Utilisé pour la propagation d'événements.
        :return: les scènes de la fenêtre.
        """
        return self._scenes

    # FPS

    @staticmethod
    def get_fps() -> float:
        """
        Renvoie le nombre de FPS actuel de la fenêtre.
        :return: le nombre de FPS actuel de la fenêtre.
        """

        # on récupère la fonction responsable du rafraichissement de la fenêtre
        refresh_func = pyglet.app.event_loop._redraw_windows  # NOQA

        # on récupère l'événement correspondant dans l'horloge de l'application
        refresh_event = next(filter(
            lambda item: item.func is refresh_func,
            itertools.chain(
                pyglet.clock._default._schedule_interval_items,  # NOQA
                pyglet.clock._default._schedule_items  # NOQA
            )
        ))

        # renvoie infini s'il n'y avait pas de fréquence, sinon 1 / fréquence pour avoir le nombre de FPS
        return inf if isinstance(refresh_event, pyglet.clock._ScheduledItem) else 1 / refresh_event.interval  # NOQA

    @staticmethod
    def set_fps(value: float):
        """
        Définit le nombre de FPS de la fenêtre.
        :param value: nombre de FPS souhaité
        """

        # on récupère la fonction responsable du rafraichissement de la fenêtre
        refresh_func = pyglet.app.event_loop._redraw_windows  # NOQA

        # désactive le rafraichissement de la fenêtre
        pyglet.clock.unschedule(refresh_func)

        if value == inf:
            # si la valeur est infinie, rafraichi dès que possible
            pyglet.clock.schedule(refresh_func)
        else:
            # sinon rafraichi à la fréquence indiquée (1 / FPS)
            pyglet.clock.schedule_interval(refresh_func, 1 / value)

    # Scene Managing

    def set_scene(self, scene_class: Type["Scene"], **scene_kwargs) -> "Scene":
        """
        Défini la scène actuelle pour la fenêtre.
        :scene_class: la classe de la scène à ajouter
        :scene_kwargs: les arguments clés de la scène
        :return: la nouvelle scène créée
        """

        self.clear_scene()
        return self.add_scene(scene_class, **scene_kwargs)

    def add_scene(self, scene_class: Type["Scene"], priority: int = 0, **scene_kwargs) -> "Scene":
        """
        Ajoute une scène à la fenêtre.
        :scene_class: la classe de la scène à ajouter
        :scene_kwargs: les arguments clés de la scène
        :return: la nouvelle scène créée
        """

        scene: "Scene" = scene_class(window=self, **scene_kwargs)
        self._scenes.insert(priority, scene)
        return scene

    def remove_scene(self, scene: "Scene") -> None:
        """
        Retire une scène spécifique de la fenêtre
        :scene: la scène à retirer
        """

        self._scenes.remove(scene)

    def clear_scene(self) -> None:
        """
        Retire toutes les scènes de la fenêtre.
        """

        self._scenes.clear()

    # Base Event

    def on_draw(self):  # NOQA
        self.clear()
