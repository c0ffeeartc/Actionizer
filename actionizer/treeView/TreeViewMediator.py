from treeView.view.TreeView import TreeView
from notifications import Notes
from puremvc.patterns.mediator import Mediator

__author__ = 'cfe'


class TreeViewMediator(Mediator):
    NAME = "TreeViewMediator"

    def __init__(self):
        super(TreeViewMediator, self).__init__(TreeViewMediator.NAME, TreeView())
        self.__tree_view = self.viewComponent

    def listNotificationInterests(self):
        return [
            Notes.TREE_MODEL_CHANGED,
        ]

    def handleNotification(self, note):
        if note.name == Notes.TREE_MODEL_CHANGED:
            self.__tree_view.update(note.body["action_root"])
