from dataclasses import dataclass
import socket

from source.network.packet.abc import Packet


@dataclass
class PacketBoatPlaced(Packet):
    def to_bytes(self):
        return b""

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls()

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "PacketBoatPlaced":
        return cls.from_bytes(connection.recv(0))
