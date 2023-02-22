from queue import Queue
from threading import Thread
from typing import Any, Callable

import pyglet


class StoppableThread(Thread):
    """
    A thread that can be stopped.
    The run method need to check for the "self._stop" variable and return manually if it is true.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True


def in_pyglet_context(func: Callable, *args, **kwargs) -> Any:
    """
    This function can be call in a thread. It will call the "func" in the pyglet event loop, avoiding
    some operation that are not allowed outside of the pyglet context, and return its result
    :param func: the function to call in the pyglet context
    :param args: the args of the function
    :param kwargs: the kwargs of the function
    :return: the result of the function
    """

    queue = Queue()
    pyglet.clock.schedule_once(lambda dt: queue.put(func(*args, **kwargs)), 0)
    return queue.get()
