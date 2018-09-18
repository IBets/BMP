from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class WidgetGraphic(FigureCanvas):
    def __init__(self, gist):
        fig = Figure()
        self.gist = gist
        self.axes = fig.add_subplot(111)

        super().__init__(fig)
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Expanding)
        self.x_line = [x for x in range(256)]

    def draw_red(self):
        self.axes.cla()
        self.axes.plot(self.x_line, self.gist.red, 'r')
        self.draw()

    def draw_green(self):
        self.axes.cla()
        self.axes.plot(self.x_line, self.gist.green, 'r')
        self.draw()

    def draw_blue(self):
        self.axes.cla()
        self.axes.plot(self.x_line, self.gist.blue, 'r')
        self.draw()

    def draw_common(self):
        self.axes.cla()
        self.axes.plot(self.x_line, self.gist.commn, 'r')
        self.draw()


class WidgetBMPHistogram(QWidget):
    def __init__(self, gist):
        super().__init__()

        widget = WidgetGraphic(gist)
        hbox = QHBoxLayout()
        vbox_button = QVBoxLayout()
        buttn_red = QPushButton("Red")
        buttn_green = QPushButton("Green")
        buttn_blue = QPushButton("Blue")
        buttn_common = QPushButton("Common")
        spacing = QLabel()
        vbox_button.addWidget(buttn_red)
        vbox_button.addWidget(buttn_green)
        vbox_button.addWidget(buttn_blue)
        vbox_button.addWidget(buttn_common)
        vbox_button.addWidget(spacing)

        hbox.addWidget(widget)
        hbox.addLayout(vbox_button)

        buttn_red.clicked.connect(lambda _: widget.draw_red())
        buttn_green.clicked.connect(lambda _: widget.draw_green())
        buttn_blue.clicked.connect(lambda _: widget.draw_blue())
        buttn_common.clicked.connect(lambda _: widget.draw_common())
        widget.show()

        self.setLayout(hbox)
        self.setWindowTitle("Гистограмма")
