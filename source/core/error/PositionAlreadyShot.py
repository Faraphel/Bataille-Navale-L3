class PositionAlreadyShot(Exception):
    def __init__(self, position: tuple[int, int]):
        super().__init__(f"The position {position} have already been shot.")

