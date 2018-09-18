from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *


class WidgetBITMAPFILEHEADER(QWidget):
    """
    Класс виджета структуры BITMAPFILEHEADER
    """
    def __init__(self, header):
        super().__init__()
        self.form_layout = QFormLayout()    
        index = 0
        for i in header.get():
            self.form_layout.setWidget(index, QFormLayout.LabelRole, QLabel(str(i[0])))
            self.form_layout.setWidget(index, QFormLayout.FieldRole, QLabel(str(i[1])))
            index+=1
        self.setLayout(self.form_layout)


class WidgetBMPHeader(QWidget):
    """
    Класс виджета BMPHeader
    Устанавливает текущий виджет 
    виджетом версией структуры полученной в header
    """
    def __init__(self, header):
        super().__init__()
        widget = WidgetBITMAPFILEHEADER(header)
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(widget)
        vbox.addLayout(hbox)
        widget.show()
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowTitle("Файловый заголовок")
        self.setLayout(vbox)
