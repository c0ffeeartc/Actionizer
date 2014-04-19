from puremvc.patterns.mediator import Mediator
from view.mainWindow.MainWindow import MainWindow

__author__ = 'cfe'


class MainWindowMediator(Mediator):
    NAME = "MainWindowMediator"

    def onRegister(self):
        super(MainWindowMediator, self).onRegister()
        self.setViewComponent(MainWindow())
