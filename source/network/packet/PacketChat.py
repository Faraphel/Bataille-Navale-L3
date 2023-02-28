from dataclasses import dataclass, field

from source.network.packet.abc import VariableLengthBytesPacket


@dataclass
class PacketChat(VariableLengthBytesPacket):
    """
    A packet that represent a message from the chat
    """

    message: str = field()

    @property
    def data(self) -> bytes:
        return self.message.encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes) -> "PacketChat":
        return cls(message=data.decode("utf-8"))
