from src import Boat


class InvalidBoatPosition(Exception):
    def __init__(self, boat: Boat, position: tuple[int, int]):
        super().__init__(f"The boat {boat} can't be placed at {position}.")
