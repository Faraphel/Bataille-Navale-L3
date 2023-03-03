from source.network.packet.abc import SignalPacket


class PacketQuit(SignalPacket):
    """
    A packet that is sent when the player wish to quit a game.
    """
