import struct

from dataclasses import dataclass, field

from source.network.packet.abc import SimplePacket
from source.type import Point2D


@dataclass
class PacketBombPlaced(SimplePacket):
    """
    Un packet qui signale qu'une bombe à été placé sur la grille
    """

    position: Point2D = field()

    packet_format: str = ">BB"

    def to_bytes(self) -> bytes:
        x, y = self.position
        return struct.pack(self.packet_format, x, y)

    @classmethod
    def from_bytes(cls, data: bytes) -> "PacketBombPlaced":
        x, y = struct.unpack(cls.packet_format, data)
        return cls(position=(x, y))
