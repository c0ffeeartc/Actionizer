from actionTree.TreeModelProxy import TreeModelProxy
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
            Notes.TREE_MODEL_SAVE,
            Notes.TREE_MODEL_ADD,
            Notes.TREE_MODEL_REMOVE,
        ]

    def handleNotification(self, note):

        tree_model_proxy = self.facade.retrieveProxy(TreeModelProxy.NAME)

        if note.name == Notes.TREE_MODEL_CHANGED:
            self.__tree_view.clear()
            self.__tree_view.update(note.body["root"])
        elif note.name == Notes.TREE_MODEL_SAVE:
            tree_model_proxy.save()
        elif note.name == Notes.TREE_MODEL_REMOVE:
            if "indexes" in note.body.keys():
                indexes = note.body["indexes"]
                tree_model_proxy.remove(*indexes)

    def get_indexes(self, tree_item):
        """:rtype :list of int"""
        return self.__tree_view.get_indexes(tree_item)

    def get_cur_item(self):
        """:rtype :PySide.QtGui.QTreeWidgetItem.QTreeWidgetItem"""
        return self.__tree_view.currentItem()

