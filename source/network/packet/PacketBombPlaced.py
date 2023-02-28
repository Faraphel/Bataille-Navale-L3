import struct

from dataclasses import dataclass, field

from source.network.packet.abc import Packet
from source.type import Point2D


@dataclass
class PacketBombPlaced(Packet):
    """
    A packet that signal that a bomb have been placed on the board
    """

    position: Point2D = field()

    packet_format: str = ">BB"

    def to_bytes(self):
        x, y = self.position
        return struct.pack(self.packet_format, x, y)

    @classmethod
    def from_bytes(cls, data: bytes):
        x, y = struct.unpack(cls.packet_format, data)
        return cls(position=(x, y))
