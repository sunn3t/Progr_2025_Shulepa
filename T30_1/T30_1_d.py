import unittest


def matrix_stats(matrix):
    """
    Повертає кортеж (total, minimum, maximum) для елементів матриці.
    matrix: список списків чисел.
    """
    if not matrix or not any(matrix):
        raise ValueError("Матриця порожня або некоректна")
    total = 0
    minimum = None
    maximum = None
    for row in matrix:
        for elem in row:
            if minimum is None or elem < minimum:
                minimum = elem
            if maximum is None or elem > maximum:
                maximum = elem
            total += elem
    return total, minimum, maximum


class TestMatrixStats(unittest.TestCase):
    def test_small_matrix(self):
        mat = [[1, 2], [3, 4]]
        self.assertEqual(matrix_stats(mat), (10, 1, 4))

    def test_mixed_values(self):
        mat = [[-1, 0, 1], [2, -2, 3]]
        self.assertEqual(matrix_stats(mat), (3, -2, 3))

    def test_single_row(self):
        mat = [[5, 5, 5]]
        self.assertEqual(matrix_stats(mat), (15, 5, 5))

    def test_single_column(self):
        mat = [[7], [8], [9]]
        self.assertEqual(matrix_stats(mat), (24, 7, 9))

    def test_rectangular_matrix(self):
        mat = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(matrix_stats(mat), (21, 1, 6))

    def test_empty_matrix(self):
        with self.assertRaises(ValueError):
            matrix_stats([])
        with self.assertRaises(ValueError):
            matrix_stats([[], []])


if __name__ == '__main__':
    unittest.main()
