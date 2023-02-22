from dataclasses import dataclass, field

from source.network.packet.abc import Packet
from source.type import Point2D


@dataclass
class PacketBombPlaced(Packet):
    """
    A packet that signal that a bomb have been placed on the board
    """

    position: Point2D = field()

    packet_size: int = 2

    def to_bytes(self):
        x, y = self.position
        return x.to_bytes(1, "big") + y.to_bytes(1, "big")

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(position=(
            int.from_bytes(data[0:1], "big"),
            int.from_bytes(data[1:2], "big"),
        ))
