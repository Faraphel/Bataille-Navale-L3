import socket
from dataclasses import dataclass, field

from source.core.enums import BombState
from source.network.packet.abc import Packet
from source.type import Point2D


@dataclass
class PacketBombState(Packet):
    position: Point2D = field()
    bomb_state: BombState = field()

    def to_bytes(self):
        x, y = self.position

        return (
            x.to_bytes(1, "big") +
            y.to_bytes(1, "big") +
            self.bomb_state.value.to_bytes()
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(
            position=(
                int.from_bytes(data[0:1], "big"),
                int.from_bytes(data[1:2], "big"),
            ),
            bomb_state=BombState.from_bytes(data[2:3])
        )

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "PacketBombState":
        return cls.from_bytes(connection.recv(3))
