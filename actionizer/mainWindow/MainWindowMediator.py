from actionTree.TreeModelProxy import TreeModelProxy
from notifications.notes import Notes
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

    def listNotificationInterests(self):
        return[
            Notes.STEP_CONTEXT_MENU_SELECTED,
        ]

    def handleNotification(self, note):
        if note.name == Notes.STEP_CONTEXT_MENU_SELECTED:
            # replaces step
            step_uid = note.body["step_uid"]
            tree = self.get_main_window().tree
            old_item = tree.currentItem()
            item_parent = old_item.parent()
            old_item_index = old_item.parent().indexOfChild(old_item)
            item_parent.removeChild(old_item)
            self.get_main_window().add_step(step_uid, item_parent, old_item_index)
        elif note.name == Notes.TREE_MODEL_SAVE:
            tree_model_proxy = self.facade.retrieveProxy(TreeModelProxy.NAME)
            tree_model_proxy.save()

    def get_main_window(self):
        return self.viewComponent
