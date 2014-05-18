from actionTree.model.Action import Action

__author__ = 'cfe'


class TreeNode(object):
    """
    Holds leaf object and its children of specified type.
    Can insert, pop and clear children.
    """
    NAME = "TreeNode"

    def __init__(self, leaf, children_type_name=None):
        self.name = ''
        self.leaf = leaf
        self.parent = None
        self.children = []
        self.children_type_names = []
        if children_type_name:
            self.children_type_names.append(children_type_name)

    def add(self, child, i=None):
        """
        Insert child within container bounds
        :type child:TreeNode
        """
        if child.leaf.NAME in self.children_type_names:
            # fix i
            len_items = len(self.children)
            if i is None or i > len_items:
                i = len_items
            elif i < 0:
                i = 0
            # insert child
            self.children.insert(i, child)
            self.children[i].parent = self

    def play(self):
        if self.leaf.NAME == Action.NAME:
            self.leaf.play(self.children)

    def remove(self, i):
        """
        Pop child for valid i
        :rtype :TreeNode
        """
        if len(self.children) > i >= 0:
            return self.children.pop(i)

    def clear(self):
        del self.children[:]

    def move(self, from_i, to_i):
        if to_i < len(self.children) and from_i <= len(self.children):
            self.children.insert(to_i, self.children.pop(from_i))

    def move_up(self, i):
        last = len(self.children) - 1
        if last >= i > 0:
            self.move(i, i - 1)

    def move_down(self, i):
        last = len(self.children) - 1
        if last > i >= 0:
            self.move(i, i + 1)

    def __getitem__(self, i):
        return self.children[i]

    def get_index(self):
        if self.parent:
            return self.parent.children.index(self)
        else:
            return None  # root node

    def get_indexes(self):
        target = self
        indexes = []
        while target.parent:
            i = target.get_index()
            indexes.insert(0, i)
            target = target.parent
        return indexes

    def jsonify(self):
        return {
            "__class__": TreeNode.NAME,
            "__value__":
            {
                "name": self.name,
                "leaf": self.leaf.jsonify(),
                "children": self.children,
                "children_type_names": self.children_type_names,
            }
        }

    @classmethod
    def dejsonify(cls, o, obj_hook):
        if o['__class__'] == TreeNode.NAME:
            leaf = o["__value__"]["leaf"]
            cont = TreeNode(leaf)
            cont.children = [child_node for child_node in o["__value__"]["children"]]
            cont.children_type_names = o["__value__"]["children_type_names"]
            return cont
