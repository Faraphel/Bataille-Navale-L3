import unittest

import numpy as np

from source.core import Board, Boat
from source.core.enums import Orientation, BombState
from source.core.error import InvalidBoatPosition, InvalidBombPosition, PositionAlreadyShot


class TestCore(unittest.TestCase):
    """
    Unité de test pour tester l'implémentation du jeu.
    """

    def test_boats(self):
        """
        Test pour le placement des bateaux
        """

        board = Board(width=5, height=5)
        board.add_boat(Boat(5, Orientation.HORIZONTAL), (0, 0))

        self.assertTrue((board.boats == np.array([
            [1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])).all())

        board.add_boat(Boat(4, Orientation.VERTICAL), (1, 1))

        self.assertTrue((board.boats == np.array([
            [1, 1, 1, 1, 1],
            [0, 2, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 2, 0, 0, 0],
        ])).all())

        self.assertRaises(
            InvalidBoatPosition,
            board.add_boat,
            Boat(3, Orientation.HORIZONTAL),
            (1, 1)
        )

        self.assertRaises(
            InvalidBoatPosition,
            board.add_boat,
            Boat(3, Orientation.HORIZONTAL),
            (4, 1)
        )

    def test_bombs(self):
        """
        Test pour le placement des bombes
        """

        board = Board(width=5, height=5)
        board.add_boat(Boat(5, Orientation.HORIZONTAL), (0, 0))
        board.add_boat(Boat(4, Orientation.VERTICAL), (1, 1))

        self.assertEqual(board.bomb((0, 0)), BombState.TOUCHED)
        self.assertEqual(board.bomb((1, 0)), BombState.TOUCHED)
        self.assertEqual(board.bomb((2, 0)), BombState.TOUCHED)
        self.assertEqual(board.bomb((3, 0)), BombState.TOUCHED)
        self.assertEqual(board.bomb((4, 0)), BombState.SUNKEN)

        self.assertEqual(board.bomb((0, 1)), BombState.NOTHING)

        self.assertRaises(
            InvalidBombPosition,
            board.bomb,
            (10, 10)
        )

        self.assertRaises(
            PositionAlreadyShot,
            board.bomb,
            (0, 0)
        )

        self.assertEqual(board.bomb((1, 1)), BombState.TOUCHED)
        self.assertEqual(board.bomb((1, 2)), BombState.TOUCHED)
        self.assertEqual(board.bomb((1, 3)), BombState.TOUCHED)
        self.assertEqual(board.bomb((1, 4)), BombState.WON)


if __name__ == '__main__':
    unittest.main()
