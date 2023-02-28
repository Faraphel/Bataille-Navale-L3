import struct
from dataclasses import dataclass, field

from source.core.enums import BombState
from source.network.packet.abc import Packet
from source.type import Point2D


@dataclass
class PacketBombState(Packet):
    """
    A packet that signal how a bomb exploded on the board
    """

    position: Point2D = field()
    bomb_state: BombState = field()

    packet_format: str = ">BBb"

    def to_bytes(self):
        x, y = self.position
        return struct.pack(self.packet_format, x, y, self.bomb_state.value)

    @classmethod
    def from_bytes(cls, data: bytes):
        x, y, bomb_state = struct.unpack(cls.packet_format, data)
        return cls(position=(x, y), bomb_state=BombState(bomb_state))
