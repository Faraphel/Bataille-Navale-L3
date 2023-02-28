import socket
import struct
from dataclasses import dataclass, field

from source.network.packet.abc import Packet


@dataclass
class PacketUsername(Packet):
    username: str = field()

    packet_format: str = ">I"

    def to_bytes(self):
        username = self.username.encode()
        username_len = len(username)

        return struct.pack(f"{self.packet_format}{username_len}s", username_len, username)

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "PacketUsername":
        username_len, *_ = struct.unpack(
            cls.packet_format,
            connection.recv(struct.calcsize(cls.packet_format))
        )

        format_: str = f">{username_len}s"

        username, *_ = struct.unpack(
            format_,
            connection.recv(struct.calcsize(format_))
        )

        return cls(username=username.decode("utf-8"))
