import sys
sys.path.append("..")

import bmp.core.header as test_header
import unittest


def open_test_file(filename):
    with open(filename, "rb") as f:
        return f.read()


class TestBMPHeader(unittest.TestCase):
    def test(self):
        file = open_test_file("test_image/1_bit.bmp")
        header = test_header.BMPHeader(file).get()
        self.assertAlmostEqual(header.type, "BM")
        self.assertAlmostEqual(header.size, 38462)
        self.assertAlmostEqual(header.reserved1, 0)
        self.assertAlmostEqual(header.reserved2, 0)
        self.assertAlmostEqual(header.off_bits, 62)


if __name__ == '__main__':
    unittest.main()
