import socket
from abc import abstractmethod, ABC
from typing import Type, Optional


class Packet(ABC):
    packed_header: bytes
    packet_id: int = 0

    def __init_subclass__(cls, **kwargs):
        cls.packet_header = Packet.packet_id.to_bytes(1, "big")
        Packet.packet_id = Packet.packet_id + 1

    @classmethod
    def cls_from_header(cls, packet_header: bytes) -> Type["Packet"]:
        return next(filter(
            lambda subcls: subcls.packet_header == packet_header,
            cls.__subclasses__()
        ))

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes) -> "Packet":
        pass

    def send_connection(self, connection: socket.socket) -> None:
        connection.send(self.packet_header)
        connection.send(self.to_bytes())

    @classmethod
    def from_connection(cls, connection: socket.socket) -> Optional[Type["Packet"]]:
        packet_header: Optional[bytes] = None
        try: packet_header = connection.recv(1)
        except socket.timeout: pass

        if not packet_header: return None

        return cls.cls_from_header(packet_header).from_connection(connection)