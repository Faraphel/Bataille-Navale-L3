from source.type import Point2D


class PositionAlreadyShot(Exception):
    def __init__(self, position: Point2D):
        super().__init__(f"The position {position} have already been shot.")

