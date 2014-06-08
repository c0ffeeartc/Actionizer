from treedataleaf.action import Action
from treedataleaf.stepitem import StepItem

__author__ = 'c0ffee'


class TreeNode(object):
    NAME = "TreeNode"
    NAME_COLUMN = 0
    LEAF_TYPE_COLUMN = 1

    def __init__(self, leaf):
        """
        @param leaf: data contained in this tree_node
        """
        self.parent_node = None
        self.name = "unnamed"
        self.is_expanded = False
        """:type :TreeNode"""
        self.leaf = leaf
        self.child_nodes = []
        """:type :list of TreeNode"""

    def add(self, node, i=None):
        if i is None:
            self.child_nodes.append(node)
            node.parent_node = self
            return
        if i < 0:
            i = 0
        elif i > len(self.child_nodes):
            i = len(self.child_nodes)
        self.child_nodes.insert(i, node)
        node.parent_node = self

    def clear(self):
        while self.child_nodes:
            self.child_nodes.pop()

    def remove(self, i=None):
        if i is None or i > len(self.child_nodes):
            i = len(self.child_nodes)
        elif i < 0:
            i = 0
        removed_node = self.child_nodes.pop(i)
        removed_node.parent_node = None
        return removed_node

    def get_type(self):
        return self.leaf.NAME

    def play(self):
        if self.leaf.NAME == Action.NAME:
            self.leaf.play(self.child_nodes)
        if self.leaf.NAME == StepItem.NAME:
            start_from_index = self.parent_node.child_nodes.index(self)
            self.parent_node.leaf.play(
                self.parent_node.child_nodes,
                start_from_index
            )

    def __getitem__(self, i):
        """:rtype :TreeNode"""
        try:
            return self.child_nodes[i]
        except IndexError:
            return None

    def get_row(self):
        if self.parent_node:
            return self.parent_node.child_nodes.index(self)
        return 0

    def get_column_count(self):
        """
        Determines number of columns in qTreeView
        Used by qAbstractModel and qTreeView
        @return:
        """
        return 2

    def get_column_data(self, i):
        """
        returns data to show in column
        @param i: column index
        @return:
        """
        if i == 0:
            return self.leaf.name
        elif i == 1:
            return self.leaf.NAME
        return "Error in get_column_data"

    def jsonify(self):
        return {
            "__class__": TreeNode.NAME,
            "__value__": {
                "name": self.name,
                "leaf": self.leaf.jsonify(),
                "child_nodes": self.child_nodes,
                # "children_type_names": self.children_type_names,
                # "is_expanded": self.is_expanded,
            }
        }

    @classmethod
    def dejsonify(cls, o):
        if o['__class__'] == TreeNode.NAME:
            leaf = o["__value__"]["leaf"]
            tree_node = TreeNode(leaf)
            """@type :TreeNode"""
            if hasattr(o["__value__"], "is_expanded"):
                tree_node.is_expanded = o["__value__"]["is_expanded"]
            if hasattr(o["__value__"], "child_nodes"):
                tree_node.child_nodes = [child_node for child_node in o["__value__"]["child_nodes"]]
                for child_node in tree_node.child_nodes:
                    child_node.parent = tree_node
            # tree_node.children_type_names = o["__value__"]["children_type_names"]
            return tree_node
