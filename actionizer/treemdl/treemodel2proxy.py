from notifications.notes import Notes
from puremvc.patterns.proxy import Proxy
from treedataleaf.actiongroup import ActionGroup
from treemdl.model.treemanager import TreeManager
from treemdl.model.treenode import TreeNode

__author__ = 'c0ffee'


class TreeModel2Proxy(Proxy):
    NAME = "TreeModel2Proxy"

    def __init__(self):
        self.__tree_manager = TreeManager()
        super(TreeModel2Proxy, self).__init__(TreeModel2Proxy.NAME, self.__tree_manager)

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

    def remove(self, q_index):
        """
        :type q_index: QModelIndex
        """
        self.__tree_manager.remove(q_index)


    def set_is_expanded(self, has_expanded, q_index):
        node = q_index.internalPointer()
        """:type :TreeNode"""
        node.set_is_expanded(has_expanded)

    def get_node(self, q_index):
        """
        :type q_index: QModelIndex
        """
        return q_index.internalPointer()

    def get_parent_q_index(self, child_node_q_index):
        return self.get_model().parent(child_node_q_index)

    def get_root(self):
        return self.__tree_manager.get_model().root_node

    def get_model(self):
        return self.__tree_manager.get_model()

    def save(self):
        self.__tree_manager.save()
        self.sendNotification(Notes.TREE_MODEL_SAVED)

    def load(self):
        print("loading")
        self.__tree_manager.load()
        self.sendNotification(Notes.TREE_MODEL_LOADED, {"root": self.__tree_manager.get_root()})
