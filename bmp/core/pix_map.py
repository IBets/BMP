import numpy


class BMPPixelMap:
    """
    Класс BMPPixelMap cодержит картупикслей изображения
    """
    def __init__(self, file, pixmap_header, pixmap_info, color_table):
        self._func_bit_color = {
            1:  self._get_1_bit_color,
            2:  self._get_2_bit_color,
            4:  self._get_4_bit_color,
            8:  self._get_8_bit_color,
            16: self._get_16_bit_color,
            24: self._get_24_bit_color,
            32: self._get_32_bit_color}

        self.info = pixmap_info
        self.color_table = color_table
        self.file = file
        self.pixel_map = numpy.arange(0, 3 * pixmap_info.height * pixmap_info.width, dtype=numpy.ubyte)
        self.index_file = pixmap_header.off_bits
        self.flag_1 = 7
        self.flag_2 = 6
        self.flag_4 = 4
        func = self._func_bit_color[pixmap_info.bit_count]
        padding = (-pixmap_info.width) & 3
        index = 0

        for i in range(pixmap_info.height):
            for j in range(pixmap_info.width):
                self.pixel_map[index], self.pixel_map[index + 1], self.pixel_map[index + 2] = func()
                index += 3

    def _get_1_bit_color(self):
        """
        Функция возращающая цвет из таблицы цветов для 1 битного изображения
        """
        buf = self.file[self.index_file]
        if self.flag_1 != 0:
            index = (buf >> self.flag_1) & 0x1
            self.flag_1 -= 1
        else:
            index = buf & 0x1
            self.index_file += 1
            self.flag_1 = 7
        return self.color_table[index]

    def _get_2_bit_color(self):
        """
        Функция возращающая цвет из таблицы цветов для 2 битного изображения
        """
        buf = self.file[self.index_file]
        if self.flag_2 != 0:
            index = (buf >> self.flag_2) & 0x3
            self.flag_2 -= 2
        else:
            index = buf & 0x3
            self.index_file += 1
            self.flag_2 = 6
        return self.color_table[index]

    def _get_4_bit_color(self):
        """
        Функция возращающая цвет из таблицы цветов для 4 битного изображения
        """
        buf = self.file[self.index_file]
        if self.flag_4 != 0:
            index = (buf >> self.flag_2) & 0xF
            self.flag_4 -= 4
        else:
            index = buf & 0xF
            self.index_file += 1
            self.flag_4 = 4
        return self.color_table[index]

    def _get_8_bit_color(self):
        """
        Функция возращающая цвет из таблицы цветов для 8 битного изображения
        """
        index_file = self.index_file
        self.index_file += 1
        return self.color_table[self.file[index_file]]

    def _get_16_bit_color(self):
        """
        Функция возращающая цвет  для 16 битного изображения
        """
        color = int.from_bytes(self.file[self.index_file:self.index_file + 2],
                               byteorder='little',
                               signed=False)
        r = (color & self.info.red_mask)   >> 7
        g = (color & self.info.green_mask) >> 2
        b = (color & self.info.blue_mask)  << 3
        self.index_file += 2
        return r, g, b

    def _get_24_bit_color(self):
        """
        Функция возращающая цвет  для 24 битного изображения
        """
        index_file = self.index_file
        self.index_file += 3
        return self.file[index_file + 2], self.file[index_file + 1], self.file[index_file]

    def _get_32_bit_color(self):
        """
        Функция возращающая цвет  для 32 битного изображения
        """
        index_file = self.index_file
        self.index_file += 4
        return self.file[index_file + 2], self.file[index_file + 1], self.file[index_file]

    def get(self):
        """
        Функция возращающая таблицу RGB
        """
        return self.pixel_map
