import socket
from abc import abstractmethod, ABC
from inspect import isabstract
from typing import Type, Optional


class Packet(ABC):
    """
    A packet that can be sent on a socket.
    Multiple subtype of packet can be sent and received in an easier way.

    The to_bytes and from_connection method need to be defined.
    """

    packet_types: set[Type["Packet"]] = set()

    packet_header: bytes
    packet_id: int = 0

    def __init_subclass__(cls, **kwargs):
        if isabstract(cls): return  # si la classe est abstraite, ignore

        cls.packet_header = Packet.packet_id.to_bytes(1, "big")  # ajoute un header à la sous-classe
        Packet.packet_id = Packet.packet_id + 1  # incrémente l'id pour que le prochain header soit différent

        cls.packet_types.add(cls)  # ajoute la sous-classe aux types de packet enregistré.

    @abstractmethod
    def to_bytes(self) -> bytes:
        """
        Convert the packet into a bytes object. The size should be "packet_size" long.
        :return: the packet encoded into a bytes.
        """
        pass

    def send_connection(self, connection: socket.socket):
        """
        Send the packet data preceded with the header directly into a socket.
        :param connection: the socket where to send the packet to.
        """
        connection.send(self.packet_header + self.to_bytes())

    def send_data_connection(self, connection: socket.socket):
        """
        Send the packet data directly into a socket.
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
            cls.packet_types
        ))

    @classmethod
    def type_from_connection(cls, connection: socket.socket) -> Optional[Type["Packet"]]:
        try:
            packet_header = connection.recv(1)
        except socket.timeout:
            return None

        if not packet_header: return None  # ignore si le header est invalide
        return cls.type_from_header(packet_header)

    @classmethod
    @abstractmethod
    def from_connection(cls, connection: socket.socket) -> "Packet":
        """
        Receive a packet from a socket.
        :param connection: the socket where to get the data from
        :return: the packet, or None if there was nothing in the socket to receive.
        """
        pass
