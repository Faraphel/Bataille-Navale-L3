import socket
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

    packet_size: int = 3

    def to_bytes(self):
        x, y = self.position

        return (
            x.to_bytes(1, "big") +
            y.to_bytes(1, "big") +
            self.bomb_state.value.to_bytes(1, "big")
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(
            position=(
                int.from_bytes(data[0:1], "big"),
                int.from_bytes(data[1:2], "big"),
            ),
            bomb_state=BombState(int.from_bytes(data[2:3], "big"))
        )
