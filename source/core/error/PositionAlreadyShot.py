from source.type import Point2D


class PositionAlreadyShot(Exception):
    """
    Erreur utilisée lorsque la bombe vise une case déjà touchée
    """

    def __init__(self, position: Point2D):
        super().__init__(f"The position {position} have already been shot.")

