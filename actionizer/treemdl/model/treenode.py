__author__ = 'c0ffee'


class TreeNode(object):
    NAME_COLUMN = 0
    LEAF_TYPE_COLUMN = 1

    def __init__(self):
        self.parent_node = None
        """:type :TreeNode"""
        self.leaf = ["name", "Node"]
        self.child_nodes = []
        """:type :list of TreeNode"""

    def add_child(self, node, i=None):
        if i is None:
            self.child_nodes.append(node)
            node.parent_node = self
            return
        if i < 0:
            i = 0
        elif i > len(self.child_nodes):
            i = len(self.child_nodes)
        self.child_nodes.insert(node, i)
        node.parent_node = self

    def remove_child(self, i=None):
        if i is None or i > len(self.child_nodes):
            i = len(self.child_nodes)
        elif i < 0:
            i = 0
        removed_node = self.child_nodes.pop(i)
        removed_node.parent_node = None
        return removed_node

    def __len__(self):
        return len(self.child_nodes)

    def __getitem__(self, i):
        """:rtype :TreeNode"""
        try:
            return self.child_nodes[i]
        except IndexError:
            return None

    def get_index(self):
        if self.parent_node:
            return self.parent_node.child_nodes.index(self)
        return 0

    def get_column_count(self):
        return 2

    def get_column_data(self, i):
        try:
            return self.leaf[i]
        except IndexError:
            return None
