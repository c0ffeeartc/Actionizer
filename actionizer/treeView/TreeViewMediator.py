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
            Notes.TREE_MODEL_LOAD,
            Notes.TREE_MODEL_SAVED,
            Notes.TREE_MODEL_LOADED,
            Notes.TREE_MODEL_ADD,
            Notes.TREE_MODEL_REMOVE,
        ]

    def handleNotification(self, note):
        tree_model_proxy = self.facade.retrieveProxy(TreeModelProxy.NAME)
        """:type :TreeModelProxy"""
        if note.name == Notes.TREE_MODEL_CHANGED:
            self.handleModelChanged(note)
        elif note.name == Notes.TREE_MODEL_SAVE:
            tree_model_proxy.save()
        elif note.name == Notes.TREE_MODEL_LOAD:
            tree_model_proxy.load()
        elif note.name == Notes.TREE_MODEL_SAVED:
            print("saved")
        elif note.name == Notes.TREE_MODEL_LOADED:
            print("updating on loaded")
            self.__tree_view.clear()
            self.__tree_view.update(note.body["root"])
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

    def handleModelChanged(self, note):
        self.__tree_view.clear()
        root_node = note.body["root"]
        """:type :TreeNode"""
        command = note.body["command"]
        """:type :str"""
        child = note.body["child"]
        """:type :TreeNode"""
        self.__tree_view.update(root_node)
