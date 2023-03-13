import unittest
import numpy as np

from source.utils import dict_filter, dict_filter_prefix, dict_add_prefix, copy_array_offset


class TestDict(unittest.TestCase):
    """
    Unité de test des fonctionnalités utilitaire pour dictionnaire
    """

    def test_dict_filter(self):
        """
        Test du filtre de dictionnaire
        """

        self.assertEqual(
            dict_filter(
                lambda key, value: key.startswith("valeur"),
                {"valeur1": 1, "valeur2": 2, "clé1": None}
            ),
            {"valeur1": 1, "valeur2": 2}
        )

        self.assertEqual(
            dict_filter(
                lambda key, value: key.startswith("test"),
                {"test_AB": 1, "TEST_AB": 2.5, "début": 3}
            ),
            {"test_AB": 1}
        )

        self.assertEqual(
            dict_filter(
                lambda key, value: key.startswith("test"),
                {"input_AB": 1, "TEST_AB": 2.5, "début": 3}
            ),
            {}
        )

    def test_dict_filter_prefix(self):
        """
        Test du filtre de dictionnaire par prefix
        """

        self.assertEqual(
            dict_filter_prefix(
                "valeur",
                {"valeur1": 1, "valeur2": 2, "clé1": None}
            ),
            {"1": 1, "2": 2}
        )

        self.assertEqual(
            dict_filter_prefix(
                "test_",
                {"test_AB": 1, "TEST_AB": 2.5, "début": 3}
            ),
            {"AB": 1}
        )

        self.assertEqual(
            dict_filter_prefix(
                "test",
                {"input_AB": 1, "TEST_AB": 2.5, "début": 3}
            ),
            {}
        )

    def test_dict_add_prefix(self):
        """
        Test de l'ajout de prefix dans un dictionnaire
        """

        self.assertEqual(
            dict_add_prefix(
                "valeur",
                {"1": 1, "2": 2, "A": None}
            ),
            {"valeur1": 1, "valeur2": 2, "valeurA": None}
        )

        self.assertEqual(
            dict_add_prefix(
                "test_",
                {"AB": 1, "2": 2.5, "fin": 3}
            ),
            {"test_AB": 1, "test_2": 2.5, "test_fin": 3}
        )

        self.assertEqual(
            dict_add_prefix(
                "test",
                {"A": 1, "B": 2.5, "E": 3}
            ),
            {"testA": 1, "testB": 2.5, "testE": 3}
        )


class TestMatrice(unittest.TestCase):
    """
    Unité de test des fonctionnalités utilitaire pour matrice
    """

    def test_copy_array_offset(self):
        """
        Test de la copie d'une matrice dans une autre avec décalage
        """

        src = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8]
        ])
        dst = np.array([
            [2, 5, 1, 3, 5, 0],
            [2, 3, 4, 1, 4, 5],
            [0, 1, 4, 0, 3, 9],
            [4, 0, 9, 5, 2, 8]
        ])

        copy_dst = dst.copy()
        copy_array_offset(src=src, dst=copy_dst, offset=(1, 2))

        self.assertTrue(
            (copy_dst == np.array([
                [2, 5, 1, 3, 5, 0],
                [2, 3, 4, 1, 4, 5],
                [0, 1, 2, 3, 4, 9],
                [4, 5, 6, 7, 8, 8]
            ])).all()
        )

        copy_dst = dst.copy()
        copy_array_offset(src=src, dst=copy_dst, offset=(2, 2))

        self.assertTrue(
            (copy_dst == np.array([
                [2, 5, 1, 3, 5, 0],
                [2, 3, 4, 1, 4, 5],
                [0, 1, 1, 2, 3, 4],
                [4, 0, 5, 6, 7, 8]
            ])).all()
        )

        copy_dst = dst.copy()
        copy_array_offset(src=src, dst=copy_dst, offset=(1, 0))

        self.assertTrue(
            (copy_dst == np.array([
                [2, 1, 2, 3, 4, 0],
                [2, 5, 6, 7, 8, 5],
                [0, 1, 4, 0, 3, 9],
                [4, 0, 9, 5, 2, 8]
            ])).all()
        )


if __name__ == '__main__':
    unittest.main()
