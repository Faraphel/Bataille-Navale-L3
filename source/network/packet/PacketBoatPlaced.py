from dataclasses import dataclass

from source.network.packet.abc import SimplePacket


@dataclass
class PacketBoatPlaced(SimplePacket):
    """
    A packet that signal that all the boat of the player have been placed
    """

    def to_bytes(self) -> bytes:
        return b""

    @classmethod
    def from_bytes(cls, data: bytes) -> "PacketBoatPlaced":
        return cls()
