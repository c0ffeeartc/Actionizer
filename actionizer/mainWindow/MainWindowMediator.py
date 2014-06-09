from mainWindow.NewTreeElementCommand import NewTreeElementCommand
from notifications.notes import Notes
from puremvc.patterns.facade import Facade
from puremvc.patterns.mediator import Mediator
from mainWindow.MainWindow import MainWindow
from treeview2.treeview2mediator import TreeView2Mediator

__author__ = 'cfe'


class MainWindowMediator(Mediator):
    NAME = "MainWindowMediator"

    def __init__(self):
        self.__treeView = Facade.getInstance().retrieveMediator(TreeView2Mediator.NAME).viewComponent
        """@type :TreeView2"""
        self.__main = MainWindow(self.__treeView)
        """@type :MainWindow"""
        super(MainWindowMediator, self).__init__(MainWindowMediator.NAME, self.__main)

        self.__main.btn_play_pressed.connect(self.on_play_pressed)
        self.__main.btn_remove_pressed.connect(self.on_remove_pressed)
        self.__main.btn_new_pressed.connect(self.on_new_pressed)
        self.__main.btn_save_pressed.connect(self.on_save_pressed)

    def on_play_pressed(self):
        self.facade.sendNotification(Notes.TREE_ITEM_PLAY)

    def on_remove_pressed(self):
        Facade.getInstance().sendNotification(Notes.TREE_MODEL_REMOVE)

    def on_new_pressed(self):
        Facade.getInstance().sendNotification(NewTreeElementCommand.NAME)

    def on_save_pressed(self):
        Facade.getInstance().sendNotification(Notes.TREE_MODEL_SAVE)
