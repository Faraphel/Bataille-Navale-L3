from enum import Enum


class Orientation(Enum):
    """
    Les possibles orientations pour un bateau
    """

    HORIZONTAL = "H"
    VERTICAL = "V"

    def to_json(self) -> str:
        return str(self.value)

    @classmethod
    def from_json(cls, json_: str) -> "Orientation":
        return cls(json_)
