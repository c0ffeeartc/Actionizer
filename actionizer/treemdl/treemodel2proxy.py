from puremvc.patterns.proxy import Proxy
from treemdl.model.treemodel import TreeModel

__author__ = 'c0ffee'


class TreeModel2Proxy(Proxy):
    NAME = "TreeModel2Proxy"

    def __init__(self):
        self.__tree = TreeModel()
        super(TreeModel2Proxy, self).__init__(TreeModel2Proxy.NAME, self.__tree)

    def add(self, node, index):
        """
        :type node: TreeNode
        :type index: QModelIndex
        """
        self.__tree.root_node.add_child(node)

    def remove(self, index):
        """
        :type index: QModelIndex
        """
        pass

    def get_node(self, index):
        """
        :type index: QModelIndex
        """
        pass
