from abc import ABC
import socket
from typing import TypeVar

from source.network.packet.abc import Packet


T = TypeVar("T", bound="SignalPacket")


class SignalPacket(Packet, ABC):
    """
    Un packet ne contenant aucune donnée.
    Permet de réagir à des événements seulement avec le type de la classe.
    """

    def to_bytes(self) -> bytes:
        return b""

    @classmethod
    def from_connection(cls, connection: socket.socket) -> T:
        return cls()
