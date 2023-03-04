import struct
from dataclasses import field, dataclass

from source.network.packet.abc import SimplePacket


@dataclass
class PacketResponseSave(SimplePacket):
    """
    A packet that is sent when the player accept or refuse a requested save.
    """

    value: bool = field()  # True si requête accepter, sinon False

    packet_format = ">?"

    def to_bytes(self) -> bytes:
        return struct.pack(self.packet_format, self.value)

    @classmethod
    def from_bytes(cls, data: bytes) -> "PacketResponseSave":
        value, *_ = struct.unpack(cls.packet_format, data)
        return cls(value=value)
