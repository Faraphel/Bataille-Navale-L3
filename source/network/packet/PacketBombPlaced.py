import socket
from dataclasses import dataclass, field

from source.network.packet.abc import Packet
from source.type import Point2D


@dataclass
class PacketBombPlaced(Packet):
    position: Point2D = field()

    def to_bytes(self):
        x, y = self.position
        return x.to_bytes(1, "big") + y.to_bytes(1, "big")

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(position=(
            int.from_bytes(data[0:1], "big"),
            int.from_bytes(data[1:2], "big"),
        ))

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "PacketBombPlaced":
        return cls.from_bytes(connection.recv(2))
