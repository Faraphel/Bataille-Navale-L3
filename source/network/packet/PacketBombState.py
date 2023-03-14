import struct
from dataclasses import dataclass, field

from source.core.enums import BombState
from source.network.packet.abc import SimplePacket
from source.type import Point2D


@dataclass
class PacketBombState(SimplePacket):
    """
    Un packet qui signale qu'une bombe à explosé sur la grille
    """

    position: Point2D = field()
    bomb_state: BombState = field()

    packet_format: str = ">BBb"

    def to_bytes(self) -> bytes:
        x, y = self.position
        return struct.pack(self.packet_format, x, y, self.bomb_state.value)

    @classmethod
    def from_bytes(cls, data: bytes) -> "PacketBombState":
        x, y, bomb_state = struct.unpack(cls.packet_format, data)
        return cls(position=(x, y), bomb_state=BombState(bomb_state))
