class InvalidBombPosition(Exception):
    def __init__(self, position: tuple[int, int]):
        super().__init__(f"The bomb can't be placed at {position}.")
