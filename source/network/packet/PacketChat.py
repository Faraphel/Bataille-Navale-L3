import socket
import struct
from dataclasses import dataclass, field
from typing import Optional

from source.network.packet.abc import Packet


@dataclass
class PacketChat(Packet):
    """
    A packet that represent a message from the chat
    """

    message: str = field()

    packet_format = ">I"

    def to_bytes(self) -> bytes:
        message: bytes = self.message.encode("utf-8")
        message_len: int = len(message)

        # envoie la taille du message, suivi des données du message
        return struct.pack(f"{self.packet_format}{message_len}s", message_len, message)

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "Packet":
        message_len, *_ = struct.unpack(
            cls.packet_format,
            connection.recv(struct.calcsize(cls.packet_format))
        )

        format_: str = f">{message_len}s"

        message, *_ = struct.unpack(
            format_,
            connection.recv(struct.calcsize(format_))
        )

        return cls(message=message.decode("utf-8"))
