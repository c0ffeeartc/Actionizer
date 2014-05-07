from model.actionTree.view import TreeView
from notifications import Notes
from puremvc.patterns.mediator import Mediator

__author__ = 'cfe'


class TreeViewMediator(Mediator):
    NAME = "TreeViewMediator"

    def __init__(self, treeView):
        super(TreeViewMediator, self).__init__(TreeViewMediator.NAME, TreeView(actionRoot))

    def listNotificationInterests(self):
        return [
            Notes.TREE_MODEL_CHANGED,
        ]

    def getTreeView(self):
        return self.viewComponent

    def handleNotification(self, note):
        if note.name == Notes.TREE_MODEL_CHANGED:
            self.getTreeView().update()
