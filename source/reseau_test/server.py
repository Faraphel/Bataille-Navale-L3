import json
import socket

from source.core.Board import Board

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 7878))
    s.listen()
    conn, addr = s.accept()

    message = conn.recv(1024)
    conn.send(b"SALUT")

    print(conn, addr, message)

    board_json = json.loads(message)
    print(Board.from_json(board_json))

