from dataclasses import dataclass

from source.network.packet.abc import SignalPacket


@dataclass
class PacketAskSave(SignalPacket):
    """
    Un packet envoyé quand le joueur souhaite sauvegarder
    """
