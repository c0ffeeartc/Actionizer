__author__ = 'c0ffee'

from PySide import QtGui


class OptionsWindow(QtGui.QWidget):
    """
    Widget with list of selectable elements and set options area corresponding to selected element
    """
    def __init__(self, *args, **kwargs):
        super(OptionsWindow, self).__init__(*args, **kwargs)

        self.__h_layout = QtGui.QHBoxLayout()
        self.__list = QtGui.QListWidget()
        self.__h_layout.addWidget(self.__list)

        self.setLayout(self.__h_layout)
