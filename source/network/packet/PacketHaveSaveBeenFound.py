import struct
from dataclasses import field, dataclass

from source.network.packet.abc import SimplePacket


@dataclass
class PacketHaveSaveBeenFound(SimplePacket):
    """
    Un packet indiquant si le joueur à trouvé un ancien fichier de sauvegarde avec l'opposant
    """

    value: bool = field()  # True si requête accepter, sinon False

    packet_format = ">?"

    def to_bytes(self) -> bytes:
        return struct.pack(self.packet_format, self.value)

    @classmethod
    def from_bytes(cls, data: bytes) -> "PacketHaveSaveBeenFound":
        value, *_ = struct.unpack(cls.packet_format, data)
        return cls(value=value)

