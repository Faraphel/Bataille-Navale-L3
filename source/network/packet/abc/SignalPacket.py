from abc import ABC
import socket
from typing import TypeVar

from source.network.packet.abc import Packet


T = TypeVar("T", bound="SignalPacket")


class SignalPacket(Packet, ABC):
    """
    A packet that has for only usage to send a signal thanks to the type of the class.
    It does not hold any other data.
    """

    def to_bytes(self) -> bytes:
        return b""

    @classmethod
    def from_connection(cls, connection: socket.socket) -> T:
        return cls()
