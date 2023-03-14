from dataclasses import dataclass, field

from source.network.packet.abc import VariableLengthPacket


@dataclass
class PacketChat(VariableLengthPacket):
    """
    Un packet qui représente un message du chat
    """

    message: str = field()

    @property
    def data(self) -> bytes:
        return self.message.encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> "PacketChat":
        return cls(message=data.decode("utf-8"))
