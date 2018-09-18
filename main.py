from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from bmp.image import ImageBMP, ImageBMPError
from gui.widget_view import GLWidget
from gui.widget_info import WidgetBMPInfo
from gui.widget_header import WidgetBMPHeader
from gui.widget_histogram import WidgetBMPHistogram

__author__ = 'Mikhal Gorobets'
__version__ = '0.1'

TITLE = "BMP"
WIDTH = 1024
HEIGHT = 800

RESOURCE = "resource/"

RES_ICON = "%sicon.png" % RESOURCE
RES_BACK_GROUND = "background-image:url(%sback_ground.jpg);" % RESOURCE


class MainWindow(QMainWindow):


    def __init__(self):

        super().__init__()

        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu('Файл')
        self.btn_open_file = QAction('Открыть')
        self.btn_exit = QAction('Выход')
        self.file_menu.addAction(self.btn_open_file)
        self.file_menu.addAction(self.btn_exit)

        self.info = self.menubar.addMenu("Информация")
        self.btn_header = QAction("О файле")
        self.btn_info = QAction("О картинке")
        self.info.addAction(self.btn_header)
        self.info.addAction(self.btn_info)

        self.histogram = self.menubar.addAction("Гистограмма")

        self.btn_open_file.triggered.connect(self.open_file)
        self.btn_info.triggered.connect(lambda _: self.info_widget.show())
        self.btn_header.triggered.connect(lambda _: self.header_widget.show())
        self.btn_exit.triggered.connect(lambda _: exit())
        self.histogram.triggered.connect(lambda _: self.histogram_wiget.show())

        self.setStyleSheet(RES_BACK_GROUND + "; background-attachment: fixed")
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(RES_ICON))
        self.info.setEnabled(False)
        self.histogram.setEnabled(False)
        self.resize(WIDTH, HEIGHT)

    def open_file(self):

        try:
            file_name = QFileDialog.getOpenFileName(self, 'Открыть файл')[0]
            file = open(file_name, "rb")
            image = ImageBMP(file.read())
            self.image_widget = GLWidget(image)
            self.header_widget = WidgetBMPHeader(image.header)
            self.info_widget = WidgetBMPInfo(image.info)
            self.histogram_wiget = WidgetBMPHistogram(image.histogram)
            self.setCentralWidget(self.image_widget)
            file.close()
        except ImageBMPError as err:
            self.show_error(err)
        except Exception as err:
            self.show_error(err)
        else:
            self.info.setEnabled(True)
            self.histogram.setEnabled(True)

    def show_error(self, text):

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(str(text))
        self.msg.setWindowTitle("Ошибка")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self,"Выход",
                                     "Вы действительно хотите выйти?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
