import unittest
import calculator

class Tests(unittest.TestCase):

    def test_1(self):
        self.assertEqual(calculator.solver(
            [[3],[3],[3],[1,1,1],[2,2]],
            [[2],[3,1],[4],[3,1],[2]],
            0)[1],
            [[0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 0], [1, 0, 1, 0, 1], [1, 1, 0, 1, 1]],
            "")

    def test_2(self):
        self.assertEqual(calculator.solver(
            [[1,2],[1,1,1],[1,1,1],[2,1]],
            [[3],[1,1],[2],[1,1],[3]],
            0)[1],
            [[0, 1, 0, 1, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 1, 0, 1, 0]],
            "")

    def test_3(self):
        self.assertEqual(calculator.solver(
            [[4],[3,3],[4,4],[4,4],[4,4],[10],[3,3],[6],[2],[1]],
            [[4],[6],[7],[8],[1,1,1,1],[1,1,2],[9],[7],[6],[4]],
            0)[1],
            [[0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 0, 0, 1, 1, 1, 0], [1, 1, 1, 1, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 1, 1, 1, 0, 0, 1, 1, 1, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]],
            "")


    def test_4(self):
        self.assertEqual(calculator.solver(
            [[3],[3],[3],[0],[2,2]],
            [[1],[1],[3],[3,1],[3,1]],
            0)[1],
            [[0, 0, 1, 1, 1], [0, 0, 1, 1, 1], [0, 0, 1, 1, 1], [0, 0, 0, 0, 0], [1, 1, 0, 1, 1]],
            "")

    def test_5(self):
        self.assertEqual(calculator.solver(
            [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]],
            [[0], [5], [0], [5], [0]],
            0)[1],
            [[0, 1, 0, 1, 0], [0, 1, 0, 1, 0], [0, 1, 0, 1, 0], [0, 1, 0, 1, 0], [0, 1, 0, 1, 0]],
            "")

    def test_6(self):
        self.assertEqual(calculator.solver(
            [[1, 1, 6], [1, 2, 1], [1, 1, 1, 2, 1], [1, 2, 2, 1], [5, 1], [7], [2, 1], [2, 1, 1, 2], [2, 2], [8]],
            [[1, 1, 1, 2], [1, 2, 3], [1, 1, 1, 2, 1], [1, 4, 1], [6, 1, 1], [1, 1, 1], [1, 2, 1, 1, 1], [1, 2, 1, 2], [1, 1, 2], [8]],
            0)[1],
            [[1, 0, 1, 0, 1, 1, 1, 1, 1, 1], [0, 1, 0, 1, 1, 0, 0, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1, 1, 0, 1], [0, 1, 0, 1, 1, 0, 1, 1, 0, 1], [1, 1, 1, 1, 1, 0, 0, 0, 0, 1], [0, 0, 0, 1, 1, 1, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0, 0, 0, 0, 1], [0, 1, 1, 0, 1, 0, 1, 0, 1, 1], [1, 1, 0, 0, 0, 0, 0, 1, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]],
            "")

    def test_7(self):
        self.assertEqual(calculator.solver(
        [[1,1],[1,3,1],[3,3],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1],[4,3],[5,3]],
        [[0],[1],[2],[10],[1,2],[9],[1],[9],[1,2],[10]],
        0)[1],
        [[0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 1, 1, 1, 0, 1], [0, 0, 0, 1, 1, 1, 0, 1, 1, 1], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 1, 1, 1, 1, 0, 1, 1, 1], [0, 1, 1, 1, 1, 1, 0, 1, 1, 1]],
        "")

if __name__ == '__main__':
    unittest.main()