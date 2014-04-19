from PySide import QtGui

__author__ = 'cfe'


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QtGui.QWidget()
        self.widget.resize(250, 150)
        self.widget.setWindowTitle('Simple')
        self.widget.show()
