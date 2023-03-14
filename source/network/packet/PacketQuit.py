from dataclasses import dataclass

from source.network.packet.abc import SignalPacket


@dataclass
class PacketQuit(SignalPacket):
    """
    Un packet envoyé lorsque le joueur souhaite quitter la partie
    """
