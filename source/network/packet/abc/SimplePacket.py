import socket
import struct
from abc import ABC, abstractmethod
from typing import TypeVar

from source.network.packet.abc import Packet


T = TypeVar("T", bound="SimplePacket")


class SimplePacket(Packet, ABC):
    """
    A packet with a simple packet format.
    Only the from_bytes and to_bytes method need to be implemented.
    """

    packet_format: str = ">"

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> T:
        """
        Convert a bytes object into a packet.
        :param data: the data to convert into a packet. Should be "packet_size" long.
        :return: a packet corresponding to the bytes.
        """
        pass

    @classmethod
    def from_connection(cls, connection: socket.socket) -> T:
        # récupère la taille du packet en fonction du format et charge
        # les données dans une nouvelle instance.
        packet_size: int = struct.calcsize(cls.packet_format)
        return cls.from_bytes(connection.recv(packet_size))
