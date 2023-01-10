import json
import socket

from source.core.Board import Board
from source.core.Boat import Boat
from source.core.enums import Orientation


board = Board(5)
board.add_boat(Boat(3, Orientation.VERTICAL), (0, 4))
board.add_boat(Boat(4, Orientation.HORIZONTAL), (4, 1))
board.bomb((2, 2))

board_json = json.dumps(board.to_json())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 7878))

    s.send(board_json.encode())

    data = s.recv(1024)

    print(data)
