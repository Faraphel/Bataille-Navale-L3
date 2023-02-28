import socket
import struct
from abc import abstractmethod, ABC
from typing import Type, Optional


class Packet(ABC):
    packed_header: bytes
    packet_id: int = 0
    packet_format: str = ">"

    def __init_subclass__(cls, **kwargs):
        cls.packet_header = Packet.packet_id.to_bytes(1, "big")  # give a header to the newly created subclass
        Packet.packet_id = Packet.packet_id + 1  # increment by one the packet header for the next subclass

    @abstractmethod
    def to_bytes(self) -> bytes:
        """
        Convert the packet into a bytes object. The size should be "packet_size" long.
        :return: the packet encoded into a bytes.
        """
        pass

    def send_connection(self, connection: socket.socket):
        """
        Send the packet directly into a socket.
        :param connection: the socket where to send the packet to.
        """
        connection.send(self.packet_header + self.to_bytes())

    def instance_send_connection(self, connection: socket.socket):
        """
        Send the packet directly into a socket.
        :param connection: the socket where to send the packet to.
        """
        connection.send(self.to_bytes())

    @classmethod
    def type_from_header(cls, packet_header: bytes) -> Type["Packet"]:
        """
        Get a subclass from its packet header.
        :param packet_header: the header to find the corresponding subclass
        :return: the class associated with this header
        """
        return next(filter(
            lambda subcls: subcls.packet_header == packet_header,
            cls.__subclasses__()
        ))

    @classmethod
    def from_bytes(cls, data: bytes) -> "Packet":
        """
        Convert a bytes object into a packet.
        :param data: the data to convert into a packet. Should be "packet_size" long.
        :return: a packet corresponding to the bytes.
        """
        pass

    @classmethod
    def type_from_connection(cls, connection: socket.socket) -> Optional[Type["Packet"]]:
        try:
            packet_header = connection.recv(1)
        except socket.timeout:
            return None

        if not packet_header: return None  # ignore si le header est invalide
        return cls.type_from_header(packet_header)

    @classmethod
    def from_connection(cls, connection: socket.socket) -> "Packet":
        """
        Receive a packet from a socket.
        :param connection: the socket where to get the data from
        :return: the packet, or None if there was nothing in the socket to receive.
        """

        packet_size: int = struct.calcsize(cls.packet_format)
        return cls.from_bytes(connection.recv(packet_size))
