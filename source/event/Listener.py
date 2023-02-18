from typing import Callable


class Listener:
    def __init__(self):
        self._events_listener: dict[str, set[Callable]] = {}

    def add_listener(self, name: str, callback: Callable):
        if name not in self._events_listener: self._events_listener[name] = set()
        self._events_listener[name].add(callback)

    def remove_listener(self, name: str, callback: Callable):
        self._events_listener[name].remove(callback)

    def trigger_event(self, name: str, *args, **kwargs):
        for listener in self._events_listener.get(name, set()):
            listener(*args, **kwargs)
