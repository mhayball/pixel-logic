import unittest
import calculator

class Tests(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_1(self):
        self.assertEqual(calculator.solver([[3],[3],[3],[1,1,1],[2,2]], [[2],[3,1],[4],[3,1],[2]], 0), [[0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1]], "")


if __name__ == '__main__':
    unittest.main()