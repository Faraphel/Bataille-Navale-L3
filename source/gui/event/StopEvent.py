class StopEvent(Exception):
    """
    Cette erreur peut être levée pour arrêter la propagation de l'événement aux autres éléments
    """
    pass
