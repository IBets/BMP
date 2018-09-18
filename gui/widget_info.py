from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from bmp.core.info   import CIEXYZTRIPLE_GAMMA


class WidgetCIEXYZTRIPLE_GAMMA(QWidget):
    """
    Класс виджета структуры CIEXYZTRIPLE_GAMMA
    """
    def __init__(self, struct):

        super().__init__()
       
        grid_layout = QGridLayout()
        index = 0
        color_label = QLabel("Red:"), QLabel("Green:"), QLabel("Blue:")
        vec_label   = QLabel("X"), QLabel("Y"), QLabel("Z")
        gamma_label = QLabel("Gamma red:"), QLabel("Gamma green:"), QLabel("Gamma blue:")

        greed = struct.ciexyz_red, struct.ciexyz_green, struct.ciexyz_blue
        gamma = struct.gamma_red,  struct.gamma_green,  struct.gamma_blue
       
        for e in range(1, 4):      
            grid_layout.addWidget(color_label[e-1],  e, 0, 1, 1)
            grid_layout.addWidget(vec_label[e-1], 0, e, 1, 1)
            grid_layout.addWidget(gamma_label[e-4],  e + 3, 0, 1, 1)
           
        for x in range(1, 4):
            for y in range(1, 4):
                field = "{0:f}".format(greed[x-1][y-1])
                grid_layout.addWidget(QLabel(field), x, y, 1, 1)

        for e in range(4, 7):
            field = "{0:f}".format(gamma[e-4])
            grid_layout.addWidget(QLabel(field), e, 1, 1, 1)

        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Конечные точки гамма")
        self.setLayout(grid_layout)
        self.show()

     
class WidgeBITMAPCOREHEADER(QWidget):
    """
    Класс виджета структуры BITMAPCOREHEADER
    """
    def __init__(self, info):

        super().__init__()
        self.form_layout = QFormLayout()    
        index = 0
        for i in info.get():
            self.form_layout.setWidget(index, QFormLayout.LabelRole, QLabel(str(i[0])))
            self.form_layout.setWidget(index, QFormLayout.FieldRole, QLabel(str(i[1])))
            index+=1
        self.setLayout(self.form_layout)


class WidgetBITMAPINFOHEADER(QWidget):
    """
    Класс виджета структуры BITMAPINFOHEADER
    """
    def __init__(self, info):

        super().__init__()
        self.form_layout = QFormLayout()    
        index = 0
        for i in info.get():
            self.form_layout.setWidget(index, QFormLayout.LabelRole, QLabel(str(i[0])))
            self.form_layout.setWidget(index, QFormLayout.FieldRole, QLabel(str(i[1])))
            index+=1
        self.setLayout(self.form_layout)


class WidgetBITMAPV4HEADER(QWidget):
    """
    Класс виджета структуры BITMAPV4HEADER
    """
    def __init__(self, info):

        super().__init__()
        self.form_layout = QFormLayout()
        self.but = QPushButton("...")
        index = 0
        for i in info.get():
            if not isinstance(i[1], CIEXYZTRIPLE_GAMMA):
                self.form_layout.setWidget(index, QFormLayout.LabelRole, QLabel(str(i[0])))
                self.form_layout.setWidget(index, QFormLayout.FieldRole, QLabel(str(i[1])))
            else: 
                self.form_layout.setWidget(index, QFormLayout.LabelRole, QLabel(str(i[0])))
                self.form_layout.setWidget(index, QFormLayout.FieldRole, self.but)
            
                self.but.clicked.connect(lambda _: self.show_struct_widget(i[1]))
            index+=1
        self.setLayout(self.form_layout)

    def show_struct_widget(self, struct):
        widget = WidgetCIEXYZTRIPLE_GAMMA(struct)
        widget.show()


class WidgetBITMAPV5HEADER(QWidget):
    """
    Класс виджета структуры BITMAPV5HEADER
    """
    def __init__(self, info):

        super().__init__()
        self.form_layout = QFormLayout()
        self.but = QPushButton("...")
        index = 0
        for i in info.get():
            if not isinstance(i[1], CIEXYZTRIPLE_GAMMA):
                self.form_layout.setWidget(index, QFormLayout.LabelRole, QLabel(str(i[0])))
                self.form_layout.setWidget(index, QFormLayout.FieldRole, QLabel(str(i[1])))
            else: 
                self.form_layout.setWidget(index, QFormLayout.LabelRole, QLabel(str(i[0])))
                self.form_layout.setWidget(index, QFormLayout.FieldRole, self.but)
                self.but.clicked.connect(lambda _: self.show_struct_widget(i[1]))
            index+=1
        self.setLayout(self.form_layout)

    def show_struct_widget(self, struct):
        """
        Метод отображающий стуктуру CIEXYZTRIPLE_GAMMA
        param struct: структура типа CIEXYZTRIPLE_GAMMA
        """ 

        widget = WidgetCIEXYZTRIPLE_GAMMA(struct)
        widget.show()


class WidgetBMPInfo(QWidget):
    """
    Класс виджета BMPinfo
    Устанавливает текущий виджет 
    виджетом версией структуры полученной в info
    """
    VERSION = {
            'Core': WidgeBITMAPCOREHEADER,
            '3': WidgetBITMAPINFOHEADER,
            '4': WidgetBITMAPV4HEADER,
            '5': WidgetBITMAPV5HEADER}

    def __init__(self, info):
        super().__init__()
        widget = WidgetBMPInfo.VERSION[info.version](info)
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(widget)
        vbox.addLayout(hbox)
        widget.show()
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Информация об изображении")
        self.setLayout(vbox)
