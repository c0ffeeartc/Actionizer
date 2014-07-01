__author__ = 'c0ffee'

from PySide import QtGui


class OptionsWindow(QtGui.QDialog):
    """
    Widget with list of selectable elements and set options area corresponding to selected element
    """
    def __init__(self, *args, **kwargs):
        super(OptionsWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Options")
        self.__main_layout = QtGui.QGridLayout()
        self.__main_layout.setColumnMinimumWidth(0, 40)
        self.__main_layout.setColumnStretch(1, 1)
        self.__list = QtGui.QListWidget()
        self.__list2 = QtGui.QListWidget()
        self.__main_layout.addWidget(self.__list, 0, 0)
        self.__main_layout.addWidget(self.__list2, 0, 1, 1, 2)

        self.setLayout(self.__main_layout)
        self.__list.addItem("Main")
        self.__list.addItem("Remap keys")
