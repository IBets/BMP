import io

class CIEXYZTRIPLE_GAMMA:
    """
    Класс структуры CIEXYZTRIPLE_GAMMA
    """
    def __init__(self, arr):

        loc_ =  self._cnv_to_CIEXYZTRIPLE(arr[0:36])

        self.ciexyz_red   = loc_[0]
        self.ciexyz_green = loc_[1]
        self.ciexyz_blue  = loc_[2]

        self.gamma_red    = self._cnv_FXPT16DOT16_to_float(arr[36:40])
        self.gamma_green  = self._cnv_FXPT16DOT16_to_float(arr[40:44])
        self.gamma_blue   = self._cnv_FXPT16DOT16_to_float(arr[44:48])


    def _cnv_FXPT2DOT30_to_float(self, byte_array):
        """
        Функция конвертирования байтов  в которых число с фиксированной точкой
        типа FXPT2DOT30 в тип float
        :param value: FXPT2DOT30
        :return:      FXPT2DOT30->float
        """
        integer = (byte_array[0] >> 6) & 0x03
        byte_array[0] = (byte_array[0] & 0x3F)
        real = int.from_bytes(byte_array[0:4], byteorder='big', signed=False) / 2**30
        return integer + real

    def _cnv_FXPT16DOT16_to_float(self, byte_array):
        """
        Функция конвертирования байтов  в которых число с фиксированной точкой
        типа FXPT16DOT16 в тип float
        :param value: FXPT16DOT16
        :return:      FXPT16DOT16->float
        """
        integer = int.from_bytes(byte_array[0:2], byteorder='big', signed=False)
        real    = int.from_bytes(byte_array[2:4], byteorder='big', signed=False) / 2 ** 16
        return integer + real

    def _cnv_to_CIEXYZ(self, array_byte):
        """
        Функция конвертирования байтов  в которых структура
        типа CIEXYZ в (x, y, z)
        :param value: CIEXYZ
        :return:      CIEXYZ->(x, y, z)
        """
        x = self._cnv_FXPT2DOT30_to_float(array_byte[0:4])
        y = self._cnv_FXPT2DOT30_to_float(array_byte[4:8])
        z = self._cnv_FXPT2DOT30_to_float(array_byte[8:12])
        return (x, y, z)

    def _cnv_to_CIEXYZTRIPLE(self, array_byte):
        """
        Функция конвертирования байтов  в которых структура
        типа CIEXYZTRIPLE в ((x,y,z),(x,y,z), (x,y,z))
        :param value: CIEXYZTRIPLE
        :return:      CIEXYZTRIPLE->((x,y,z),(x,y,z), (x,y,z))
        """
        red   = self._cnv_to_CIEXYZ(array_byte[0:12])
        green = self._cnv_to_CIEXYZ(array_byte[12:24])
        blue  = self._cnv_to_CIEXYZ(array_byte[24:36])
        return (red, green, blue)


class BITMAPCOREHEADER:
    """
    Класс структуры BITMAPCOREHEADER
    """
    def __init__(self, file):
      
        file = io.BytesIO(file)
        file.seek(0x0E)
        self.size      = self._cnv_to_int(file.read(4))
        self.width     = self._cnv_to_int(file.read(2))
        self.height    = self._cnv_to_int(file.read(2))
        self.planes    = self._cnv_to_int(file.read(2))
        self.bit_count = self._cnv_to_int(file.read(2))

   
    def get(self):
        """
        Возвращает (Название поля, Значегие поля)
       
        """
        result = [("Размер заголовка байтах:",      self.size),
                  ("Ширина заголовка в байтах",     self.width),
                  ("Ширина изображения в пикселях", self.height),
                  ("Количество плоскостей",         self.planes),
                  ("Количество бит на пиксель",     self.bit_count)]

        return result

    def _cnv_to_int(self, value):
        """
        Функция конвертирования байтов  в int
        :param value: Массив байт
        :return:      Перекорвертивроанные байты в тип int
        """
        return int.from_bytes(value, byteorder='little', signed=False)

    @property
    def version(self):
        """
        Свойство возвращающее векрсию структуры
        """
        return 'Core'


class BITMAPINFOHEADER:
    """
    Класс структуры BITMAPINFOHEADER
    """
    COMPRESSION = {
            0: 'BI_RGB',
            1: 'BI_RLE8',
            2: 'BI_RLE4',
            3: 'BI_BITFIELDS',
            4: 'BI_JPEG',
            5: 'BI_PNG',
            6: 'BI_ALPHABITFIELDS'}

    DEF_MASK_16 = {
            'red':   0x7C00,
            'green': 0x03E0,
            'blue':  0x001F,
            'alpha': 0x0000}

    DEF_MASK_32 = {
            'red':   0x00FF0000,
            'green': 0x0000FF00,
            'blue':  0x000000FF,
            'alpha': 0x00000000}
       
    def __init__(self, file):
      
        self.io_file = io.BytesIO(file)
        self.io_file.seek(0x0E)
        self.size          = self._cnv_to_int(self.io_file.read(4))
        self.width         = self._cnv_to_int(self.io_file.read(4))
        self.height        = self._cnv_to_int(self.io_file.read(4))
        self.planes        = self._cnv_to_int(self.io_file.read(2))
        self.bit_count     = self._cnv_to_int(self.io_file.read(2))
        self.compression   = self._cnv_to_int(self.io_file.read(4))
        self.size_image    = self._cnv_to_int(self.io_file.read(4))
        self.x_ppm         = self._cnv_to_int(self.io_file.read(4))
        self.y_ppm         = self._cnv_to_int(self.io_file.read(4))
        self.clr_user      = self._cnv_to_int(self.io_file.read(4))
        self.clr_important = self._cnv_to_int(self.io_file.read(4))

        self.red_mask   = None
        self.green_mask = None
        self.blue_mask  = None
        self.alpha_mask = None

        self._set_default_mask()

        if self.compression == 'BI_BITFIELDS':
            self.red_mask   = self._cnv_to_int(self.io_file.read(4))
            self.green_mask = self._cnv_to_int(self.io_file.read(4))
            self.blue_mask  = self._cnv_to_int(self.io_file.read(4))
            if self.size == 40:
                self.size += 12
        if self.compression == 'BI_ALPHABITFIELDS':
            self.red_mask   = self._cnv_to_int(self.io_file.read(4))
            self.green_mask = self._cnv_to_int(self.io_file.read(4))
            self.blue_mask  = self._cnv_to_int(self.io_file.read(4))
            self.alpha_mask = self._cnv_to_int(self.io_file.read(4))
            if self.size == 40:
                self.size += 16

    @property
    def version(self):
        """
        Свойство возвращающее векрсию структуры
        """
        return '3'

    @property
    def compression(self):
        """
        Свойство возвращающее тип конпрессии указанной в COMPRESSION
        """
        return self._compression

    @compression.setter
    def compression(self, value):
        self._compression = BITMAPINFOHEADER.COMPRESSION[value]

    @property
    def clr_user(self):
        """
        Свойство возвращающее размер таблицы цветов
        """
        return self._clr_user

    @clr_user.setter
    def clr_user(self, value):
        if value != 0 or self.bit_count > 8:
            self._clr_user = value
        else:
            self._clr_user = 2 ** self.bit_count

    def _set_default_mask(self):   
        """
        Метод устанавливающий маску по умолчанию,
        если глубина цвета 16 и 32 бита из DEF_MASK_16, DEF_MASK_32

        """ 
        if self.bit_count == 16:
            self.red_mask   = BITMAPINFOHEADER.DEF_MASK_16['red']
            self.green_mask = BITMAPINFOHEADER.DEF_MASK_16['green']
            self.blue_mask  = BITMAPINFOHEADER.DEF_MASK_16['blue']
            self.alpha_mask = BITMAPINFOHEADER.DEF_MASK_16['alpha']
        if self.bit_count == 32:
            self.red_mask   = BITMAPINFOHEADER.DEF_MASK_32['red']
            self.green_mask = BITMAPINFOHEADER.DEF_MASK_32['green']
            self.blue_mask  = BITMAPINFOHEADER.DEF_MASK_32['blue']
            self.alpha_mask = BITMAPINFOHEADER.DEF_MASK_32['alpha']

    def _cnv_to_int(self, value):
        """
        Функция конвертирования байтов  в int
        :param value: Массив байт
        :return:      Перекорвертивроанные байты в тип int
        """
        return int.from_bytes(value, byteorder='little', signed=False)

    def get(self):
        """
        Возвращает (Название поля, Значегие поля)
       
        """

        result = [('Размер заголовка в байтах:',      self.size),
                  ('Ширина изображения в пикселях:',  self.width),
                  ('Высота изображения в пикселях:',  self.height),
                  ('Число плоскостей:',               self.planes),
                  ('Количество бит на пиксель:',      self.bit_count),
                  ('Тип компресии:',                  self.compression),
                  ('Размер пиксельных данных:',       self.size_image),
                  ('Кол-во пикселей на метр по X:',   self.x_ppm),
                  ('Кол-во пикселей на метр по Y:',   self.y_ppm),
                  ('Число используемых цветов: ',     self.clr_user),
                  ('Кол-во ячеек в таблице цветов: ', self.clr_important)]
        if self.red_mask:
            prefix = '0x{:08X}'
            result.append(('Red mask:',   prefix.format(self.red_mask)))
            result.append(('Gren mask:',  prefix.format(self.green_mask)))
            result.append(('Blue mask:',  prefix.format(self.blue_mask)))
            result.append(('Alpha mask:', prefix.format(self.alpha_mask)))
        return result

class BITMAPV4HEADER(BITMAPINFOHEADER):
    """
    Класс структуры BITMAPV4HEADER
    """
    CS_TYPE = {
            0:          'LCS_CALIBRATED_RGB',
            0x73524742: 'LCS_sRGB',
            0x57696E20: 'LCS_WINDOWS_COLOR_SPACE',
            0x4C494E4B: 'PROFILE_LINKED',
            0x4D424544: 'PROFILE_EMBEDDED'}

    def __init__(self, file):

        super().__init__(file)

        self.io_file.seek(0x36)
        self.red_mask   = self._cnv_to_int(self.io_file.read(4))
        self.green_mask = self._cnv_to_int(self.io_file.read(4))
        self.blue_mask  = self._cnv_to_int(self.io_file.read(4))
        self.alpha_mask = self._cnv_to_int(self.io_file.read(4))
        self.cs_type    = self._cnv_to_int(self.io_file.read(4))
        if self.cs_type == 'LCS_CALIBRATED_RGB':
            self.struct  = CIEXYZTRIPLE_GAMMA(self.io_file.read(48))

    @property
    def cs_type(self):
        """
        Свойство возвращающее тип цветового пространства из CS_TYPE
        """
        return self._cs_type

    @cs_type.setter
    def cs_type(self, value):  
        self._cs_type = BITMAPV4HEADER.CS_TYPE[value]
    
    def generator(self):
        """
        Функция генератор
        Возвращает (Название поля, Значегие поля)
       
        """
        result = BITMAPINFOHEADER.get(self)
        result.append(('Вид цветового пространства:', self.cs_type))  
        if self.cs_type == 'LCS_CALIBRATED_RGB':
            result.append(('Конечные точки гамма', self.struct)) 
        return result

    @property
    def version(self):
        """
        Свойство возвращающее векрсию структуры
        """
        return '4'


class BITMAPV5HEADER(BITMAPV4HEADER):
    """
    Класс структуры BITMAPV5HEADER
    """
    RENDERING_INTENS = {
            1: 'LCS_GM_BUSINESS',
            2: 'LCS_GM_GRAPHICS',
            4: 'LCS_GM_IMAGES',
            8: 'LCS_GM_ABS_COLORIMETRIC'}

    def __init__(self, file):
        super().__init__(file)
        self.io_file.seek(0x7A)
        self.intent       = self._cnv_to_int(self.io_file.read(4))
        self.profile_data = self._cnv_to_int(self.io_file.read(4))
        self.profile_size = self._cnv_to_int(self.io_file.read(4))
        self.reserved     = self._cnv_to_int(self.io_file.read(4))

    @property
    def intent(self):
        """
        Свойство возвращающее предпочтение при редеринге из RENDERING_INTENS
        """
        return self._intent

    @intent.setter
    def intent(self, value):  
        self._intent = BITMAPV5HEADER.RENDERING_INTENS[value]

    def get(self):
        """
        Функция генератор
        Возвращает (Название поля, Значегие поля)
       
        """
        result = BITMAPV4HEADER.get(self)
        result.append(("Предпочтение при рендеринге:",         self.intent))
        result.append(("Смещение в байтах цветового профиля:", self.profile_data))
        result.append(("Размер в байтах цветового провфиля:",  self.profile_size))
        result.append(("Зарезервированно:",                    self.reserved))
        return result

    @property
    def version(self):
        """
        Свойство возвращающее векрсию структуры
        """
        return '5'


class BMPInfoError(Exception):
    """
    Класс BMPInfoError
    Вызывает исключения при ошибкци иницализации  BMPInfo
    """
    pass

class BMPInfo:
    """
    Класс BMPInfo
    Содержит версию струкуры полученно из file
    """
    VERSION = {
            12: 'Core',
            40: '3',
            52: '3',
            56: '3',
            108:'4',
            124:'5'}

    BITMAP_INFO = {
            'Core': BITMAPCOREHEADER,
            '3':    BITMAPINFOHEADER,
            '4':    BITMAPV4HEADER,
            '5':    BITMAPV5HEADER}

    def __init__(self, file):
        try:
            prefix = int.from_bytes(file[0x0E:0x12],byteorder='little',signed=False)
            ver = BMPInfo.VERSION[prefix] 
            self.bmp_info = BMPInfo.BITMAP_INFO[ver](file)
        except Exception:
            raise BMPInfoError("Размер заголовка не совпадает с форматом .bmp")
       
    def get(self):
        """
        Функция возвращающее текущуб структуру
        """
        return self.bmp_info

    @property
    def version(self):
        """
        Свойство возвращающее векрсию структуры
        """
        return self.bmp_info.version
