import socket
from abc import abstractmethod, ABC
from typing import Type, Optional


class Packet(ABC):
    packed_header: bytes
    packet_size: int
    packet_id: int = 0

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

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> "Packet":
        """
        Convert a bytes object into a packet.
        :param data: the data to convert into a packet. Should be "packet_size" long.
        :return: a packet corresponding to the bytes.
        """
        pass

    @classmethod
    def cls_from_header(cls, packet_header: bytes) -> Type["Packet"]:
        """
        Get a subclass from its packet header.
        :param packet_header: the header to find the corresponding subclass
        :return: the class associated with this header
        """
        return next(filter(
            lambda subcls: subcls.packet_header == packet_header,
            cls.__subclasses__()
        ))

    def send_connection(self, connection: socket.socket):
        """
        Send the packet directly into a socket.
        :param connection: the socket where to send the packet to.
        """
        connection.send(self.packet_header + self.to_bytes())

    @classmethod
    def cls_from_connection(cls, connection: socket.socket) -> Optional[Type["Packet"]]:
        """
        Receive a packet type from a socket.
        :param connection: the socket where to get the header from
        :return: the packet class, or None if there was nothing in the socket to receive.
        """
        packet_header: Optional[bytes] = None
        try:
            packet_header = connection.recv(1)
        except socket.timeout:
            pass

        return cls.cls_from_header(packet_header) if packet_header else None  # ignore si le header est invalide

    @classmethod
    def instance_from_connection(cls, connection: socket.socket) -> Optional["Packet"]:
        """
        Receive a packet instance data from a socket.
        :param connection: the socket where to get the data from
        :return: the packet, or None if there was nothing in the socket to receive.
        """
        return cls.from_bytes(connection.recv(cls.packet_size))

    @classmethod
    def from_connection(cls, connection: socket.socket) -> Optional[Type["Packet"]]:
        """
        Receive a packet from a socket.
        :param connection: the socket where to get the data from
        :return: the packet, or None if there was nothing in the socket to receive.
        """
        subcls = cls.cls_from_connection(connection)
        return None if subcls is None else subcls.instance_from_connection(connection)
