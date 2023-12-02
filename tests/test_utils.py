import unittest
import sys
from utils import clamp_valid_number


class TestClampValidNumber(unittest.TestCase):
    def test_normal_valid(self):
        for x in range(-100, 100):
            with self.subTest(x=x):
                y = clamp_valid_number(x)
                self.assertEqual(x, y)

    def test_normal_nan(self):
        self.assertIsNone(clamp_valid_number(float('nan')))

    def test_normal_inf(self):
        self.assertEqual(clamp_valid_number(float('inf')), sys.float_info.max)
        self.assertEqual(clamp_valid_number(-float('inf')), -sys.float_info.max)


if __name__ == '__main__':
    unittest.main()
