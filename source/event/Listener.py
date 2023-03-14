from typing import Callable


class Listener:
    """
    Les classes héritant de Listener permettent d'ajouter, retirer et appeler facilement des événements.
    """

    def __init__(self):
        # dictionnaire des événements et de leurs fonctions associées
        self._events_listener: dict[str, set[Callable]] = {}

    def add_listener(self, name: str, callback: Callable):
        """
        Ajoute une fonction à un événement
        :param name: le nom de l'événement
        :param callback: la fonction à appeler
        """
        if name not in self._events_listener: self._events_listener[name] = set()
        self._events_listener[name].add(callback)

    def remove_listener(self, name: str, callback: Callable):
        """
        Retire une fonction d'un événement
        :param name: le nom de l'événement
        :param callback: la fonction à retirer
        """
        self._events_listener[name].remove(callback)

    def trigger_event(self, name: str, *args, **kwargs):
        """
        Appelle les fonctions associées à un événement
        :param name: le nom de l'événement
        :param args: les arguments des fonctions
        :param kwargs: les arguments à clé des fonctions
        """

        # .copy() pour que si le listener supprime un de ses événements, la liste de la boucle de change pas de taille
        for listener in self._events_listener.get(name, set()).copy():
            listener(self, *args, **kwargs)
