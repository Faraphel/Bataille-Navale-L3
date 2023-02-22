from dataclasses import dataclass
import socket

from source.network.packet.abc import Packet


@dataclass
class PacketBoatPlaced(Packet):
    packet_size: int = 0

    def to_bytes(self):
        return b""

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls()
