from queue import Queue
from threading import Thread
from typing import Any, Callable

import pyglet


class StoppableThread(Thread):
    """
    Un thread pouvant être arrêté.
    La méthode "run" doit souvent vérifier la variable self.stopped et faire un return manuellement si cette variable
    est vrai.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stopped = False

    def stop(self) -> None:
        # indique que le thread devrait s'arrêter dès que possible
        self.stopped = True


def in_pyglet_context(func: Callable, *args, **kwargs) -> Any:
    """
    Cette fonction doit être appelée dans un thread. Elle appellera une fonction dans la boucle d'événement de pyglet,
    ce qui permet d'éviter certaines opérations illégales en dehors de ce contexte et renvoie le résultat.
    :param func: la fonction à appeler
    :param args: les arguments de la fonction
    :param kwargs: les arguments à clé de la fonction
    :return: le résultat de la fonction
    """

    queue = Queue()
    pyglet.clock.schedule_once(lambda dt: queue.put(func(*args, **kwargs)), 0)
    return queue.get()
