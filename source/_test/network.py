import socket
import string
import unittest
import random
from threading import Thread
from typing import Optional

from source.network.packet import PacketChat


class TestNetwork(unittest.TestCase):
    PORT: int = 54231

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

    def test_packet_chat(self):
        for _ in range(100):
            message = "".join(random.choice(string.printable) for _ in range(random.randint(1, 100)))

            PacketChat(message).send_data_connection(self.co_server)
            packet_chat = PacketChat.from_connection(self.co_client)

            self.assertEqual(message, packet_chat.message)

    # TODO: autre type de packets
    # TODO: type de packet générique


if __name__ == '__main__':
    unittest.main()
