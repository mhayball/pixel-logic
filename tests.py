import unittest
import calculator

class Tests(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

    def test_sum_tuple2(self):
        self.assertEqual(calculator.calculator(1), 3, "Should be 3")

class Tests2(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

    def test_sum_tuple2(self):
        self.assertEqual(calculator.calculator(1), 3, "Should be 3")

if __name__ == '__main__':
    unittest.main()