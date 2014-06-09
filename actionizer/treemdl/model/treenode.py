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
        self.__is_expanded = False
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

    def get_name(self):
        return self.leaf.name

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
        return 3

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
        elif i == 2:
            if self.get_type() == Action.NAME:
                return self.leaf.hotkey
            else:
                return ""
        return "Error in get_column_data"

    def jsonify(self):
        return {
            "__class__": TreeNode.NAME,
            "__value__": {
                "leaf": self.leaf.jsonify(),
                "child_nodes": self.child_nodes,
                # "children_type_names": self.children_type_names,
                "is_expanded": self.__is_expanded,
            }
        }

    def set_hotkey(self, new_hotkey):
        if self.get_type() == Action.NAME:
            self.leaf.hotkey = new_hotkey

    @classmethod
    def dejsonify(cls, o):
        if o['__class__'] == TreeNode.NAME:
            value = o["__value__"]
            leaf = value["leaf"]
            tree_node = TreeNode(leaf)
            """@type :TreeNode"""
            if "is_expanded" in value:
                tree_node.set_is_expanded(o["__value__"]["is_expanded"])
            if "child_nodes" in value:
                loaded_child_nodes = [child_node for child_node in value["child_nodes"]]
                for child_node in loaded_child_nodes:
                    tree_node.add(child_node)
            return tree_node

    def get_is_expanded(self):
        return self.__is_expanded

    def set_is_expanded(self, has_expanded):
        self.__is_expanded = has_expanded

    def rename(self, new_name):
        self.leaf.name = new_name
