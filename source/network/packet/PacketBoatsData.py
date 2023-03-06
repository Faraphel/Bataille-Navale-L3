import socket
import struct
from dataclasses import dataclass, field

import numpy as np

from source.network.packet.abc import Packet


@dataclass
class PacketBoatsData(Packet):

    boats: np.ndarray = field()

    packet_format: str = ">II"

    def to_bytes(self) -> bytes:
        width, height = self.boats.shape
        size: int = width * height

        return struct.pack(
            f"{self.packet_format}{size*2}s",  # deux "s" parce qu'un bateau est représenté en ushort
            width,
            height,
            self.boats.tobytes()
        )

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "PacketBoatsData":
        width, height = struct.unpack(
            cls.packet_format,
            connection.recv(struct.calcsize(cls.packet_format))
        )

        size: int = width * height
        format_ = f"{size*2}s"  # deux "s" parce qu'un bateau est représenté en ushort

        data, *_ = struct.unpack(
            format_,
            connection.recv(struct.calcsize(format_))
        )

        return cls(
            boats=np.frombuffer(data, dtype=np.ushort).reshape((width, height))
        )
