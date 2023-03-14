from dataclasses import dataclass, field

from source.network.packet.abc import VariableLengthPacket


@dataclass
class PacketUsername(VariableLengthPacket):
    """
    Un packet contenant le nom d'utilisateur de l'opposant
    """

    username: str = field()

    @property
    def data(self) -> bytes:
        return self.username.encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> "PacketUsername":
        return cls(username=data.decode("utf-8"))

