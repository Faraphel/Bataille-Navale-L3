import socket
import struct
from abc import ABC, abstractmethod
from typing import TypeVar

from source.network.packet.abc import Packet


T = TypeVar("T", bound="SimplePacket")


class SimplePacket(Packet, ABC):
    """
    Un packet avec un format plus simple.
    Se base sur le "packet_format" pour envoyé et reservoir les données.
    """

    packet_format: str = ">"

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> T:
        """
        Convertie un objet bytes en un SimplePacket
        :param data: les données à charger, doit être "packet_size" de long
        :return: un SimplePacket correspondant à ces données
        """
        pass

    @classmethod
    def from_connection(cls, connection: socket.socket) -> T:
        # récupère la taille du packet en fonction du format et charge
        # les données dans une nouvelle instance.
        packet_size: int = struct.calcsize(cls.packet_format)
        return cls.from_bytes(connection.recv(packet_size))
