from dataclasses import dataclass, field

from source.core.enums import BombState


@dataclass
class PacketBombState:
    x: int = field()
    y: int = field()
    bomb_state: BombState = field()

    def to_bytes(self) -> bytes:
        return (
            self.x.to_bytes(1, "big") +
            self.y.to_bytes(1, "big") +
            self.bomb_state.value.to_bytes()
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(
            x=int.from_bytes(data[0:1], "big"),
            y=int.from_bytes(data[1:2], "big"),
            bomb_state=BombState.from_bytes(data[2:3])
        )
