import unittest
import calculator

class Tests(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_1(self):
        self.assertEqual(calculator.solver(
            [[3],[3],[3],[1,1,1],[2,2]],
            [[2],[3,1],[4],[3,1],[2]],
            0),
            [[0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1]],
            "")

    def test_2(self):
        self.assertEqual(calculator.solver(
            [[1,2],[1,1,1],[1,1,1],[2,1]],
            [[3],[1,1],[2],[1,1],[3]],
            0),
            [[0, 1, 0, 1, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 1, 0, 1, 0]],
            "")

    def test_3(self):
        self.assertEqual(calculator.solver(
            [[4],[3,3],[4,4],[4,4],[4,4],[10],[3,3],[6],[2],[0]],
            [[4],[6],[7],[8],[1,1,1],[1,1,2],[9],[7],[6],[4]],
            0),
            ,
            "")

if __name__ == '__main__':
    unittest.main()