from actionTree.model.ActionRoot import ActionRoot
from actionTree.model.TreeManager import TreeManager
from notifications import Notes
from puremvc.patterns.proxy import Proxy

__author__ = 'cfe'


class TreeModelProxy(Proxy):
    NAME = "TreeModelProxy"

    def __init__(self):
        super(TreeModelProxy, self).__init__(TreeModelProxy.NAME)
        self.__tree = TreeManager()
        self.setData(self.__tree)

    def add(self, child, *i_list):
        self.__tree.add(child, *i_list)
        self.sendNotification(
            Notes.TREE_MODEL_ADD,
            {"child": child, "at_index": i_list, }
        )

    def remove(self, *i_list):
        self.__tree.remove(*i_list)
        self.sendNotification(
            Notes.TREE_MODEL_ADD,
            {"at_index": i_list}
        )

    def save(self):
        self.__tree.save()

    def load(self):
        self.__tree.load()
        self.sendNotification(
            Notes.TREE_MODEL_CHANGED,
            {"root": self.__tree.root}
        )

    def __getitem__(self, i):
        return self.__tree[i]
