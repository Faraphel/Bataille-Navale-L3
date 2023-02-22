from enum import Enum


class BombState(Enum):
    NOTHING = 0
    TOUCHED = 1
    SUNKEN = 2
    WON = 3

    ERROR = 10

    def to_bytes(self) -> bytes:
        return self.value.to_bytes(1, "big")

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(int.from_bytes(data, "big"))
