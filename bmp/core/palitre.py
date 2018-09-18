
class BMPPalitre:
    """
    Класс BMPPalitre cодержит палитру изображениея
    """
    def __init__(self, file, info):
        self.palitre = []
        if info.version == 'Core': self._extract_palitre_core(file, info)
        else: self._extract_palitre(file, info)

    def _extract_palitre_core(self, file, info):
        """
        Функция извлекающая палитру изображения из файла
        для версиии core
        :param file Массив байтов загружаемого файла
        :paran info Структура информации об изображении
        :return: [(r,g,b),..]
        """

        offset = info.size + 14
        for i in range(2**info.bit_count):
            buf = file[offset:offset + 3]
            self.palitre.append((buf[2], buf[1], buf[0]))
            offset += 4
        return self.palitre

    def _extract_palitre(self, file, info):
        """
        Функция извлекающая палитру изображения из файла
        для оставшихся версий
        :param file Массив байтов загружаемого файла
        :paran info Структура информации об изображении
        :return: [(r,g,b),..]
        """
        offset = info.size + 14
        for i in range(info.clr_user):
            buf = file[offset:offset + 3]
            self.palitre.append((buf[2], buf[1], buf[0]))
            offset += 4

    def get(self):
        """
        Функция возвращающая текущую палитры цветов из данного класса
        :return: [(r,g,b),..]
        """
        return self.palitre
