import socket
from dataclasses import dataclass, field

from source.network.packet.abc import Packet


@dataclass
class PacketChat(Packet):
    message: str = field()

    def to_bytes(self):
        return self.message.encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(message=data.decode("utf-8"))

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "PacketChat":
        return cls.from_bytes(connection.recv(256))