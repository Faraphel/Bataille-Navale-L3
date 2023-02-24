from dataclasses import dataclass, field

from source.network.packet.abc import Packet


@dataclass
class PacketUsername(Packet):
    username: str = field()

    packet_size: int = 16

    def to_bytes(self):
        return self.username.encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(username=data.decode("utf-8"))
