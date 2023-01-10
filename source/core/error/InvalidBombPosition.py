from source.type import Point2D


class InvalidBombPosition(Exception):
    def __init__(self, position: Point2D):
        super().__init__(f"The bomb can't be placed at {position}.")
