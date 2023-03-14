import socket
import struct
from abc import ABC, abstractmethod
from typing import TypeVar

from source.network.packet.abc import Packet


T = TypeVar("T", bound="VariableLengthPacket")


class VariableLengthPacket(Packet, ABC):
    """
    Un packet représentant une seule valeur avec une longueur variable qui peut être encodé, comme une chaîne.
    """

    packet_format: str = ">I"

    @property
    @abstractmethod
    def data(self) -> bytes:
        """
        Donnée à envoyer sur le réseau
        :return: la donnée sous la forme d'un objet bytes
        """

        pass

    def to_bytes(self) -> bytes:
        data: bytes = self.data
        data_len: int = len(data)

        # envoie la taille du message, suivi des données du message
        return struct.pack(f"{self.packet_format}{data_len}s", data_len, data)

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes):
        pass

    @classmethod
    def from_connection(cls, connection: socket.socket) -> T:
        data_len, *_ = struct.unpack(
            cls.packet_format,
            connection.recv(struct.calcsize(cls.packet_format))
        )

        format_: str = f">{data_len}s"

        data, *_ = struct.unpack(
            format_,
            connection.recv(struct.calcsize(format_))
        )

        return cls.from_bytes(data)
