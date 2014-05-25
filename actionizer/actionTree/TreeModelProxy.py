from actionTree.model.TreeManager import TreeManager
from notifications.notes import Notes, TreeNodeRenamedVO
from puremvc.patterns.facade import Facade
from puremvc.patterns.proxy import Proxy

__author__ = 'cfe'


class TreeModelProxy(Proxy):
    NAME = "TreeModelProxy"

    def __init__(self):
        super(TreeModelProxy, self).__init__(TreeModelProxy.NAME)
        self.__tree = TreeManager()
        self.setData(self.__tree)

    def add(self, child, *indexes):
        self.__tree.add(child, *indexes)
        self.sendNotification(
            Notes.TREE_MODEL_ADDED,
            {
                "child": child,
                "indexes": indexes,
                "root": self.__tree.root_node
            }
        )

    def remove(self, *i_indexes):
        self.__tree.remove(*i_indexes)
        self.sendNotification(
            Notes.TREE_MODEL_REMOVED,
            {
                "indexes": i_indexes,
                "root": self.__tree.root_node,
            }
        )

    def rename(self, new_name, *indexes):
        renamed_node = self.__tree.rename(new_name, *indexes)
        Facade.getInstance().sendNotification(
            Notes.TREE_NODE_RENAMED,
            TreeNodeRenamedVO(new_name, indexes),
        )

    def get_indexes(self, tree_node):
        return self.__tree.get_indexes(tree_node)

    def save(self):
        self.__tree.save()
        self.sendNotification(Notes.TREE_MODEL_SAVED)

    def load(self):
        print("loading")
        self.__tree.load()
        self.sendNotification(Notes.TREE_MODEL_LOADED,
                              {"root": self.__tree.root_node})

    def __getitem__(self, i):
        return self.__tree[i]
