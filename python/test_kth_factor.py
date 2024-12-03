import unittest
from kth_factor import KthFactor

class TestKthFactor(unittest.TestCase):
    def test_example_1(self):
        self.assertEqual(KthFactor().kth_factor(12, 3), 3)

    def test_example_2(self):
        self.assertEqual(KthFactor().kth_factor(7, 2), 7)

    def test_example_3(self):
        self.assertEqual(KthFactor().kth_factor(4, 4), -1)

if __name__ == '__main__':
    unittest.main()