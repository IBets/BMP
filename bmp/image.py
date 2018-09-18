from .core.pix_map import BMPPixelMap
from .core.header import BMPHeader, BMPHeaderError
from .core.info import BMPInfo, BMPInfoError
from .core.palitre import BMPPalitre
from .core.histogram import BMPHistogram


class ImageBMPError(Exception):
    pass


class ImageBMP:
    """
    Класс загружающий из файла файловый заголовок, 
                               информацию об изображении, 
                               карту пикселей
    """

    def __init__(self, file):
        try:
            self.header = BMPHeader(file).get()
            self.info = BMPInfo(file).get()
            self.palitre = BMPPalitre(file, self.info).get()
            self.pix_map = BMPPixelMap(file, self.header, self.info, self.palitre).get()
            self.histogram = BMPHistogram(self.pix_map)
        except BMPHeaderError as err:
            raise ImageBMPError(str(err))
        except BMPInfoError as err:
            raise ImageBMPError(str(err))

    @property
    def width(self):
        """
        Свойство возвращающее ширину изображения

        :return: Ширина в пикселях
        """
        return self.info.width

    @property
    def height(self):
        """
        Свойство возвращающее высоту изображения

        :return: Высота в пикселях
        """
        return self.info.height

    @property
    def version(self):
        """
        Свойство возвращающее версию заголовка BMP
        :return: Версия BMP 
        """
        return self.info.version
