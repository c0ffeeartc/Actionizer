from PySide import QtGui
import sys
from AppFacade import AppFacade

__author__ = 'cfe'


class AppMain(object):
    @staticmethod
    def main():
        facade = AppFacade.getInstance()
        app = QtGui.QApplication(sys.argv)
        facade.startup()
        sys.exit(app.exec_())


if __name__ == "__main__":
    AppMain.main()
