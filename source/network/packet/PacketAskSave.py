from dataclasses import dataclass

from source.network.packet.abc import SignalPacket


@dataclass
class PacketAskSave(SignalPacket):
    """
    A packet that is sent when the player wish to save the game.
    """
