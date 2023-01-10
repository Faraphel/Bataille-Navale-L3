import json
import socket
import sys

from source.core.Board import Board
from source.core.Boat import Boat
from source.core.enums import Orientation, BombState
from source.core.error import InvalidBoatPosition, InvalidBombPosition, PositionAlreadyShot

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 7878))

    print(f"[Client] Connecté avec {s}")

    width: int = int.from_bytes(s.recv(32), "big")
    height: int = int.from_bytes(s.recv(32), "big")

    print(width, height)

    board = Board(width, height)

    boat_count: int = int.from_bytes(s.recv(32), "big")

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

    message = s.recv(32)
    s.send(b"ready")

    print("Phase de bombardement")

    while True:

        # tour de l'adversaire

        while True:
            print("En attente du joueur adverse...")

            x = int.from_bytes(s.recv(32), "big")
            y = int.from_bytes(s.recv(32), "big")

            try:
                bomb_state = board.bomb((x, y))
                s.send(bomb_state.value.to_bytes(32, "big"))

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

        # mon tour

        while True:
            x = int(input("valeur X de la bombe ? (int) : "))
            y = int(input("valeur Y de la bombe ? (int) : "))

            s.send(x.to_bytes(32, "big"))
            s.send(y.to_bytes(32, "big"))

            bomb_state = BombState(int.from_bytes(s.recv(32), "big"))

            match bomb_state:
                case BombState.ERROR:
                    error = s.recv(1024)
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
