from typing import Callable


class Listener:
    """
    The Listener can be subclassed to allow the subclass to add, remove and call event easily.
    """

    def __init__(self):
        self._events_listener: dict[str, set[Callable]] = {}

    def add_listener(self, name: str, callback: Callable):
        """
        Add a function to an event name
        :param name: the name of the event to react
        :param callback: the function to call
        """
        if name not in self._events_listener: self._events_listener[name] = set()
        self._events_listener[name].add(callback)

    def remove_listener(self, name: str, callback: Callable):
        """
        Remove a function from an event name
        :param name: the event name where to remove the callback
        :param callback: the callback function to remove
        """
        self._events_listener[name].remove(callback)

    def trigger_event(self, name: str, *args, **kwargs):
        """
        Call all the callback attached to an event
        :param name: the name of the event to call
        :param args: the args of the callbacks
        :param kwargs: the kwargs of the callbacks
        """
        for listener in self._events_listener.get(name, set()):
            listener(*args, **kwargs)
