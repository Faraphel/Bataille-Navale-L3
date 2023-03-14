import socket
import struct
from dataclasses import dataclass, field

from source.network.packet.abc import Packet


@dataclass
class PacketSettings(Packet):
    """
    Un packet contenant tous les paramètres de la partie
    """

    grid_width: int = field()
    grid_height: int = field()
    host_start: bool = field()
    boats_length: list = field()

    packet_format: str = ">BB?I"

    def to_bytes(self) -> bytes:
        boats_len: int = len(self.boats_length)

        return struct.pack(
            f"{self.packet_format}{boats_len}B",

            self.grid_width,
            self.grid_height,
            self.host_start,

            boats_len,

            *self.boats_length
        )

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "PacketSettings":
        grid_width, grid_height, host_start, boats_len = struct.unpack(
            cls.packet_format,
            connection.recv(struct.calcsize(cls.packet_format))
        )

        format_ = f">{boats_len}B"

        boats_length = struct.unpack(
            format_,
            connection.recv(struct.calcsize(format_))
        )

        return cls(
            grid_width=grid_width,
            grid_height=grid_height,
            host_start=host_start,
            boats_length=list(boats_length)
        )
