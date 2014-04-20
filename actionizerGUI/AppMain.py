from PySide import QtGui
import sys
from AppFacade import AppFacade

__author__ = 'cfe'


class AppMain(object):
    @staticmethod
    def main():
        app = QtGui.QApplication(sys.argv)
        AppFacade.getInstance().startup()
        sys.exit(app.exec_())


if __name__ == "__main__":
    AppMain.main()
