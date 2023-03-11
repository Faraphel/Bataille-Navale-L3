from dataclasses import dataclass

from source.network.packet.abc import SignalPacket


@dataclass
class PacketBoatPlaced(SignalPacket):
    """
    A packet that signal that all the boat of the player have been placed
    """
