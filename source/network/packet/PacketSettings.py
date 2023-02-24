import struct
from dataclasses import dataclass, field

from source.network.packet.abc import Packet


@dataclass
class PacketSettings(Packet):
    username: str = field()
    grid_width: int = field()
    grid_height: int = field()
    host_start: bool = field()
    boats_length: list = field()

    packet_size: int = 51
    packet_format: str = ">16sBB?32B"

    def to_bytes(self):
        boat_size = self.boats_length + ([0] * (32 - len(self.boats_length)))

        return struct.pack(
            self.packet_format,

            self.username.encode("utf-8"),
            self.grid_width,
            self.grid_height,
            self.host_start,

            *boat_size
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        username, grid_width, grid_height, host_start, *boats_length = struct.unpack(cls.packet_format, data)

        return cls(
            username=username.replace(b"\x00", b"").decode("utf-8"),
            grid_width=grid_width,
            grid_height=grid_height,
            host_start=host_start,
            boats_length=list(filter(lambda value: value != 0, boats_length))
        )
