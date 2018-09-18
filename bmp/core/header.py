import io

class BITMAPFILEHEADER:
    """
    Класс структуры BITMAPFILEHEADER
    """
    def __init__(self, file):
       
        file = io.BytesIO(file)
        self.type = file.read(2).decode("utf-8")    
        self.size      = self._cnv_to_int(file.read(4))
        self.reserved1 = self._cnv_to_int(file.read(2))
        self.reserved2 = self._cnv_to_int(file.read(2))
        self.off_bits  = self._cnv_to_int(file.read(4))

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
        result = [('Сигнатура:',             self.type),
                  ('Размер файла в байтах:', self.size),
                  ('Зарезервированно 1:',    self.reserved1),
                  ('Зарезервированно 2:',    self.reserved2),
                  ('Адреc карты пикселей:',  self.off_bits)]
        
        return result
        

class BMPHeaderError(Exception):
    """
    Класс BMPHeaderError
    Вызывает исключения при ошибкци иницализации  BMPHeader
    """
    pass


class BMPHeader:
    """
    Класс BMPHeader
    Содержит версию струкуры полученно из file
    """
    def __init__(self, file):
        try:
            self.bmp_header = BITMAPFILEHEADER(file)
        except Exception:
            raise BMPHeaderError("Файл не BMP")

    def get(self):
        """
        Функция возвращающее текущуб структуру
        """
        return self.bmp_header
