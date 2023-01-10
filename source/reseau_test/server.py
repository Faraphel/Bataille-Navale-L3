import json
import socket
import sys

from source.core.Board import Board
from source.core.Boat import Boat
from source.core.enums import Orientation, BombState
from source.core.error import InvalidBoatPosition, InvalidBombPosition, PositionAlreadyShot

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 7878))
    s.listen()
    conn, addr = s.accept()

    print(f"[Serveur] Connecté avec {addr}")

    width: int = int(input("Largeur du plateau ? (int) : "))
    height: int = int(input("Longueur du plateau ? (int) : "))

    conn.send(width.to_bytes(32, "big"))
    conn.send(height.to_bytes(32, "big"))

    board = Board(width, height)

    boat_count: int = int(input("Nombre de bateau ? (int) : "))

    conn.send(boat_count.to_bytes(32, "big"))

    for _ in range(boat_count):
        while True:
            try:
                print(board)
                x = int(input("valeur X du bateau ? (int) : "))
                y = int(input("valeur Y du bateau ? (int) : "))
                o = input("orientation du bateau ? (H|V) : ")
                board.add_boat(Boat(3, Orientation(o)), (x, y))

            except InvalidBoatPosition:
                print("Position du bateau invalide.", file=sys.stderr)

            else:
                break

    conn.send(b"ready")
    message = conn.recv(32)

    print("Phase de bombardement")

    while True:
        # posé les bombes

        while True:
            x = int(input("valeur X de la bombe ? (int) : "))
            y = int(input("valeur Y de la bombe ? (int) : "))

            conn.send(x.to_bytes(32, "big"))
            conn.send(y.to_bytes(32, "big"))

            bomb_state = BombState(int.from_bytes(conn.recv(32), "big"))

            match bomb_state:
                case BombState.ERROR:
                    error = conn.recv(1024)
                    print(error, file=sys.stderr)

                case BombState.NOTHING:
                    print("Raté !")
                    break

                case BombState.TOUCHED:
                    print("Touché !")

                case BombState.SUNKEN:
                    print("Coulé !")

                case BombState.WON:
                    print("Gagné !")
                    break

        # tour de l'adversaire

        while True:
            print("En attente du joueur adverse...")

            x = int.from_bytes(conn.recv(32), "big")
            y = int.from_bytes(conn.recv(32), "big")

            try:
                bomb_state = board.bomb((x, y))
                conn.send(bomb_state.value.to_bytes(32, "big"))

                match bomb_state:
                    case bomb_state.NOTHING:
                        print("Raté !")
                        break

                    case BombState.TOUCHED:
                        print("Touché !")

                    case BombState.SUNKEN:
                        print("Coulé !")

                    case BombState.WON:
                        print("Perdu !")
                        break

            except (InvalidBombPosition, PositionAlreadyShot) as e:
                s.send(BombState.ERROR.value.to_bytes(32, "big"))
                s.send(f"Error : {str(e)}".encode())

