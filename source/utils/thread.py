from threading import Thread


class StoppableThread(Thread):
    """
    A thread that can be stopped.
    The run method need to check for the "self._stop" variable and return manually if it is true.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop = False

    def stop(self) -> None:
        self._stop = True
