class StopEvent(Exception):
    """
    This error can be raised to prevent an event to propagate to further element.
    """
    pass
