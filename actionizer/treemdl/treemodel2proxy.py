from notifications.notes import Notes
from puremvc.patterns.proxy import Proxy
from treedataleaf.actiongroup import ActionGroup
from treemdl.model.treemanager import TreeManager
from treemdl.model.treenode import TreeNode

__author__ = 'c0ffee'


class TreeModel2Proxy(Proxy):
    NAME = "TreeModelProxy"

    def __init__(self):
        self.__tree = TreeManager()
        super(TreeModel2Proxy, self).__init__(TreeModel2Proxy.NAME, self.__tree)
        self.get_root().add(TreeNode(ActionGroup()))
        self.get_root()[0].name = "asdf"
        self.get_root().add(TreeNode(ActionGroup()))
        self.get_root().add(TreeNode(ActionGroup()))
        self.get_root()[2].name = "3"

    def add(self, parent_node, index):
        """
        :type parent_node: TreeNode
        :type index: int
        """
        """:type :$class"""
        if parent_node is None:
            child = TreeNode(ActionGroup())
            self.get_root().add(child, 0)
            """:type :TreeNode"""

    def remove(self, *indexes):
        """
        :type index: QModelIndex
        """
        pass

    def get_node(self, index):
        """
        :type index: QModelIndex
        """
        pass

    def get_root(self):
        return self.__tree.model.root_node

    def get_model(self):
        return self.__tree.model

    def load(self):
        print("loading")
        self.__tree.load()
        root_node = self.__tree.get_root()
        self.sendNotification(Notes.TREE_MODEL_LOADED, {"root": root_node})
