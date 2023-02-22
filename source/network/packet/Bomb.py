from dataclasses import dataclass, field


@dataclass
class Bomb:
    x: int = field()
    y: int = field()

    def to_bytes(self) -> bytes:
        return (
            self.x.to_bytes(1, "big") +
            self.y.to_bytes(1, "big")
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(
            x=int.from_bytes(data[0:1], "big"),
            y=int.from_bytes(data[1:2], "big"),
        )
