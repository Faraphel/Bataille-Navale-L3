import struct
from dataclasses import field, dataclass

from source.network.packet.abc import SimplePacket


@dataclass
class PacketLoadOldSave(SimplePacket):
    """
    Un packet qui est envoyé lorsque l'hôte accepte ou refuse de charger une ancienne sauvegarde
    """

    value: bool = field()  # True si requête accepter, sinon False

    packet_format = ">?"

    def to_bytes(self) -> bytes:
        return struct.pack(self.packet_format, self.value)

    @classmethod
    def from_bytes(cls, data: bytes) -> "PacketLoadOldSave":
        value, *_ = struct.unpack(cls.packet_format, data)
        return cls(value=value)

