from dataclasses import dataclass

from source.network.packet.abc import Packet


@dataclass
class PacketBoatPlaced(Packet):
    """
    A packet that signal that all the boat of the player have been placed
    """

    def to_bytes(self):
        return b""

    @classmethod
    def from_bytes(cls, data: bytes):
        return cls()
