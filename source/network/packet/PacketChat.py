from dataclasses import dataclass, field

from source.network.packet.abc import Packet


@dataclass
class PacketChat(Packet):
    """
    A packet that represent a message from the chat
    """

    message: str = field()

    packet_size: int = 256

    def to_bytes(self) -> bytes:
        return self.message.encode("utf-8")

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls(message=data.decode("utf-8"))
