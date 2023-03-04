from source.network.packet.abc import SignalPacket


class PacketAskSave(SignalPacket):
    """
    A packet that is sent when the player wish to save the game.
    """
