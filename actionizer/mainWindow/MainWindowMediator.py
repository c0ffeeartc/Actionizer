from puremvc.patterns.facade import Facade
from puremvc.patterns.mediator import Mediator
from mainWindow.MainWindow import MainWindow
from treeView.TreeViewMediator import TreeViewMediator

__author__ = 'cfe'


class MainWindowMediator(Mediator):
    NAME = "MainWindowMediator"

    def __init__(self):
        treeView = Facade.getInstance().retrieveMediator(TreeViewMediator.NAME).viewComponent
        super(MainWindowMediator, self).__init__(MainWindowMediator.NAME, MainWindow(treeView))
