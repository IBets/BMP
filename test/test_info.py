import sys
sys.path.append("..")

import bmp.core.info as test_info
import unittest


def open_test_file(filename):
    with open(filename, "rb") as f:
        return f.read()



class TestEndPointsStruct(unittest.TestCase):


    def test_CIEXYZTRIPLE_GAMMA(self):

        test_arr = bytearray(b'\x28\xF5\xC2\x8F'
                             b'\x15\x1E\xB8\x52'
                             b'\x01\xEB\x85\x1F'
                             b'\x13\x33\x33\x33'
                             b'\x26\x66\x66\x66'
                             b'\x06\x66\x66\x66'
                             b'\x09\x99\x99\x9A'
                             b'\x03\xD7\x0A\x3D'
                             b'\x32\x8F\x5C\x29'
                             b'\x00\x02\x19\x9A'
                             b'\x00\x02\x19\x9A'
                             b'\x00\x02\x19\x9A')


        struct = test_info.CIEXYZTRIPLE_GAMMA(test_arr)

        self.assertAlmostEqual(struct.ciexyz_red[0], 0.64, delta=0.0001)
        self.assertAlmostEqual(struct.ciexyz_red[1], 0.33, delta=0.0001)
        self.assertAlmostEqual(struct.ciexyz_red[2], 0.03, delta=0.0001)

        self.assertAlmostEqual(struct.ciexyz_green[0], 0.30, delta=0.0001)
        self.assertAlmostEqual(struct.ciexyz_green[1], 0.60, delta=0.0001)
        self.assertAlmostEqual(struct.ciexyz_green[2], 0.10, delta=0.0001)

        self.assertAlmostEqual(struct.ciexyz_blue[0], 0.15, delta=0.0001)
        self.assertAlmostEqual(struct.ciexyz_blue[1], 0.06, delta=0.0001)
        self.assertAlmostEqual(struct.ciexyz_blue[2], 0.79, delta=0.0001)
        
        self.assertAlmostEqual(struct.gamma_red,   2.10,delta=0.0001)
        self.assertAlmostEqual(struct.gamma_green, 2.10,delta=0.0001)
        self.assertAlmostEqual(struct.gamma_blue,  2.10,delta=0.0001)


class TestBMPInfo(unittest.TestCase):
    def test_1_bit(self):
        file = open_test_file("test_image/1_bit.bmp")
        info = test_info.BMPInfo(file).get()

        self.assertAlmostEqual(info.size, 40)
        self.assertAlmostEqual(info.width, 640)
        self.assertAlmostEqual(info.height, 480)
        self.assertAlmostEqual(info.planes, 1)
        self.assertAlmostEqual(info.bit_count, 1)
        self.assertAlmostEqual(info.compression, "BI_RGB")
        self.assertAlmostEqual(info.size_image, 38400)
        self.assertAlmostEqual(info.x_ppm, 2835)
        self.assertAlmostEqual(info.y_ppm, 2835)
        self.assertAlmostEqual(info.clr_user, 2)
        self.assertAlmostEqual(info.clr_important, 2)

    def test_4_bit(self):
        file = open_test_file("test_image/4_bit.bmp")
        info = test_info.BMPInfo(file).get()

        self.assertAlmostEqual(info.size, 40)
        self.assertAlmostEqual(info.width, 200)
        self.assertAlmostEqual(info.height, 150)
        self.assertAlmostEqual(info.planes, 1)
        self.assertAlmostEqual(info.bit_count, 4)
        self.assertAlmostEqual(info.compression, "BI_RGB")
        self.assertAlmostEqual(info.size_image, 15000)
        self.assertAlmostEqual(info.x_ppm, 2835)
        self.assertAlmostEqual(info.y_ppm, 2835)
        self.assertAlmostEqual(info.clr_user, 16)
        self.assertAlmostEqual(info.clr_important, 0)

    def test_8_bit(self):
        file = open_test_file("test_image/8_bit.bmp")
        info = test_info.BMPInfo(file).get()

        self.assertAlmostEqual(info.size, 40)
        self.assertAlmostEqual(info.width, 800)
        self.assertAlmostEqual(info.height, 600)
        self.assertAlmostEqual(info.planes, 1)
        self.assertAlmostEqual(info.bit_count, 8)
        self.assertAlmostEqual(info.compression, "BI_RGB")
        self.assertAlmostEqual(info.size_image, 480000)
        self.assertAlmostEqual(info.x_ppm, 0)
        self.assertAlmostEqual(info.y_ppm, 0)
        self.assertAlmostEqual(info.clr_user, 256)
        self.assertAlmostEqual(info.clr_important, 256)

    def test_16_bit(self):
        file = open_test_file("test_image/16_bit.bmp")
        info = test_info.BMPInfo(file).get()
        self.assertAlmostEqual(info.size, 40)
        self.assertAlmostEqual(info.width, 699)
        self.assertAlmostEqual(info.height, 461)
        self.assertAlmostEqual(info.planes, 1)
        self.assertAlmostEqual(info.bit_count, 16)
        self.assertAlmostEqual(info.compression, "BI_RGB")
        self.assertAlmostEqual(info.size_image, 645402)
        self.assertAlmostEqual(info.x_ppm, 39)
        self.assertAlmostEqual(info.y_ppm, 39)
        self.assertAlmostEqual(info.clr_user, 0)
        self.assertAlmostEqual(info.clr_important, 0)
        self.assertAlmostEqual(info.red_mask, 0x7C00)
        self.assertAlmostEqual(info.green_mask, 0x03E0)
        self.assertAlmostEqual(info.blue_mask, 0x001F)
        self.assertAlmostEqual(info.alpha_mask, 0x0000)

    def test_24_bit(self):
        file = open_test_file("test_image/24_bit.bmp")
        info = test_info.BMPInfo(file).get()
        self.assertAlmostEqual(info.size, 124)
        self.assertAlmostEqual(info.width, 2560)
        self.assertAlmostEqual(info.height, 1440)
        self.assertAlmostEqual(info.planes, 1)
        self.assertAlmostEqual(info.bit_count, 24)
        self.assertAlmostEqual(info.compression, "BI_RGB")
        self.assertAlmostEqual(info.size_image, 11059200)
        self.assertAlmostEqual(info.x_ppm, 0)
        self.assertAlmostEqual(info.y_ppm, 0)
        self.assertAlmostEqual(info.clr_user, 0)

        self.assertAlmostEqual(info.red_mask, 0x00FF0000)
        self.assertAlmostEqual(info.green_mask, 0x0000FF00)
        self.assertAlmostEqual(info.blue_mask, 0x000000FF)
        self.assertAlmostEqual(info.alpha_mask, 0xFF000000)

        self.assertAlmostEqual(info.cs_type, "LCS_sRGB")
        self.assertAlmostEqual(info.intent, "LCS_GM_IMAGES")

        self.assertAlmostEqual(info.profile_data, 0)
        self.assertAlmostEqual(info.profile_size, 0)
        self.assertAlmostEqual(info.reserved, 0)

    def test_32_bit(self):
        file = open_test_file("test_image/32_bit.bmp")
        info = test_info.BMPInfo(file).get()
        self.assertAlmostEqual(info.size, 40)
        self.assertAlmostEqual(info.width, 699)
        self.assertAlmostEqual(info.height, 461)
        self.assertAlmostEqual(info.planes, 1)
        self.assertAlmostEqual(info.bit_count, 32)
        self.assertAlmostEqual(info.compression, "BI_RGB")
        self.assertAlmostEqual(info.size_image, 1288958)
        self.assertAlmostEqual(info.x_ppm, 39)
        self.assertAlmostEqual(info.y_ppm, 39)
        self.assertAlmostEqual(info.clr_user, 0)
        self.assertAlmostEqual(info.clr_important, 0)

        self.assertAlmostEqual(info.red_mask, 0x00FF0000)
        self.assertAlmostEqual(info.green_mask, 0x0000FF00)
        self.assertAlmostEqual(info.blue_mask, 0x000000FF)
        self.assertAlmostEqual(info.alpha_mask, 0x00000000)


if __name__ == '__main__':
    unittest.main()
