import socket
import struct
from abc import ABC, abstractmethod

from source.network.packet.abc import Packet


class VariableLengthBytesPacket(Packet, ABC):
    """
    A Packet that represent a single value that can be encoded with a variable length.
    The property "data" and the method "from_bytes" need to be defined.
    """

    packet_format: str = ">I"

    @property
    @abstractmethod
    def data(self) -> bytes:
        pass

    def to_bytes(self) -> bytes:
        data: bytes = self.data
        data_len: int = len(data)

        # envoie la taille du message, suivi des données du message
        return struct.pack(f"{self.packet_format}{data_len}s", data_len, data)

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes):
        pass

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "Packet":
        data_len, *_ = struct.unpack(
            cls.packet_format,
            connection.recv(struct.calcsize(cls.packet_format))
        )

        format_: str = f">{data_len}s"

        data, *_ = struct.unpack(
            format_,
            connection.recv(struct.calcsize(format_))
        )

        return cls.from_bytes(data)
