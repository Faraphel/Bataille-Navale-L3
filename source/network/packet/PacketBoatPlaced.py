from dataclasses import dataclass

from source.network.packet.abc import SignalPacket


@dataclass
class PacketBoatPlaced(SignalPacket):
    """
    Un packet signalant que tous les bateaux du joueur ont été placé
    """
