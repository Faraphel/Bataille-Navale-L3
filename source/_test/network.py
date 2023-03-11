import socket
import string
import unittest
import random
from threading import Thread
from typing import Optional

import numpy as np

from source.core.enums import BombState
from source.network.packet import PacketChat, PacketUsername, PacketQuit, PacketAskSave, PacketBoatPlaced, \
    PacketLoadOldSave, PacketResponseSave, PacketHaveSaveBeenFound, PacketBombPlaced, PacketBombState, PacketSettings, \
    PacketBoatsData
from source.network.packet.abc import Packet


class TestNetwork(unittest.TestCase):
    PORT: int = 54200

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Prépare deux sockets pour simuler les packets
        self.co_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.so_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.so_server.bind(("", self.PORT))
        self.so_server.listen()
        self.co_server: Optional[socket.socket] = None

        def connect_server(): self.co_server, _ = self.so_server.accept()
        def connect_client(): self.co_client.connect(("127.0.0.1", self.PORT))

        thread_server = Thread(target=connect_server)
        thread_client = Thread(target=connect_client)
        thread_server.start()
        thread_client.start()
        thread_server.join()
        thread_client.join()

    def __del__(self):
        self.co_client.close()
        self.so_server.close()

    # tous les tests de packet sont réunis dans la même fonction pour éviter de réouvrir des sockets sur le mêmes
    # ports encore et encore
    def test_packet(self):
        # PacketChat
        for _ in range(100):
            packet_sent = PacketChat(
                message="".join(random.choice(string.printable) for _ in range(random.randint(1, 100)))
            )
            packet_sent.send_data_connection(self.co_server)
            packet_recv = PacketChat.from_connection(self.co_client)

            self.assertEqual(packet_sent, packet_recv)

        # PacketUsername
        for _ in range(100):
            packet_sent = PacketUsername(
                username="".join(random.choice(string.printable) for _ in range(random.randint(1, 16)))
            )
            packet_sent.send_data_connection(self.co_server)
            packet_recv = PacketUsername.from_connection(self.co_client)

            self.assertEqual(packet_sent, packet_recv)

        # PacketQuit
        for _ in range(100):
            PacketQuit().send_data_connection(self.co_server)
            PacketQuit.from_connection(self.co_client)

        # PacketAskSave
        for _ in range(100):
            PacketAskSave().send_data_connection(self.co_server)
            PacketAskSave.from_connection(self.co_client)

        # PacketBoatPlaced
        for _ in range(100):
            PacketBoatPlaced().send_data_connection(self.co_server)
            PacketBoatPlaced.from_connection(self.co_client)

        # PacketLoadOldSave
        for _ in range(100):
            packet_sent = PacketLoadOldSave(
                value=bool(random.randint(0, 1))
            )
            packet_sent.send_data_connection(self.co_server)
            packet_recv = PacketLoadOldSave.from_connection(self.co_client)

            self.assertEqual(packet_sent, packet_recv)

        # PacketResponseSave
        for _ in range(100):
            packet_sent = PacketResponseSave(
                value=bool(random.randint(0, 1))
            )
            packet_sent.send_data_connection(self.co_server)
            packet_recv = PacketResponseSave.from_connection(self.co_client)

            self.assertEqual(packet_sent, packet_recv)

        # PacketHaveSaveBeenFound
        for _ in range(100):
            packet_sent = PacketHaveSaveBeenFound(
                value=bool(random.randint(0, 1))
            )
            packet_sent.send_data_connection(self.co_server)
            packet_recv = PacketHaveSaveBeenFound.from_connection(self.co_client)

            self.assertEqual(packet_sent, packet_recv)

        # PacketBombPlaced
        for _ in range(100):
            packet_sent = PacketBombPlaced(
                (random.randint(0, 64), random.randint(0, 64))
            )
            packet_sent.send_data_connection(self.co_server)
            packet_recv = PacketBombPlaced.from_connection(self.co_client)

            self.assertEqual(packet_sent, packet_recv)

        # PacketBombState
        for _ in range(100):
            packet_sent = PacketBombState(
                position=(random.randint(0, 64), random.randint(0, 64)),
                bomb_state=random.choice(list(BombState)),
            )
            packet_sent.send_data_connection(self.co_server)
            packet_recv = PacketBombState.from_connection(self.co_client)

            self.assertEqual(packet_sent, packet_recv)

        # PacketSettings
        for _ in range(100):
            packet_sent = PacketSettings(
                grid_width=random.randint(0, 64),
                grid_height=random.randint(0, 64),
                host_start=bool(random.randint(0, 1)),
                boats_length=[random.randint(1, 16) for _ in range(random.randint(1, 32))]
            )
            packet_sent.send_data_connection(self.co_server)
            packet_recv = PacketSettings.from_connection(self.co_client)

            self.assertEqual(packet_sent, packet_recv)

        # PacketBoatsData
        for _ in range(100):
            packet_sent = PacketBoatsData(
                boats=(
                    np.random.rand(
                        random.randint(2, 32),
                        random.randint(2, 32),
                    ) * random.randint(1, 65535)
                ).astype(dtype=np.ushort)
            )
            packet_sent.send_data_connection(self.co_server)
            packet_recv = PacketBoatsData.from_connection(self.co_client)

            self.assertTrue((packet_sent.boats == packet_recv.boats).all())  # NOQA

        # Packet Générique
        for _ in range(100):
            # prend un packet signal aléatoire (sont plus simples a initialisé)
            packet_sent_type = random.choice([PacketQuit, PacketAskSave, PacketBoatPlaced, PacketUsername, PacketChat])

            if packet_sent_type in [PacketUsername, PacketChat]:
                packet_sent = packet_sent_type(
                    "".join(random.choice(string.printable) for _ in range(random.randint(1, 16)))
                )
            else:
                packet_sent = packet_sent_type()

            packet_sent.send_connection(self.co_server)
            packet_recv_type = Packet.type_from_connection(self.co_client)
            packet_recv = packet_recv_type.from_connection(self.co_client)

            self.assertEqual(packet_recv, packet_sent)


if __name__ == '__main__':
    unittest.main()
