from dataclasses import dataclass

from source.network.packet.abc import SignalPacket


@dataclass
class PacketQuit(SignalPacket):
    """
    A packet that is sent when the player wish to quit a game.
    """
