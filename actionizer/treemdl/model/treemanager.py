import json
import errno

from options.OptionsVO import Options
from treedataleaf.Action import Action
from treedataleaf.ActionGroup import ActionGroup
from treedataleaf.ActionRoot import ActionRoot
from treedataleaf.StepItem import StepItem
from treemdl.model.treemodel import TreeModel
from treemdl.model.treenode import TreeNode


__author__ = 'c0ffee'


class TreeManager(object):
    def __init__(self):
        self.__model = TreeModel()

    def get_root(self):
        """
        :rtype :TreeNode
        """
        return self.__model.root_node

    def play(self, *indexes):
        self.get_node(*indexes).play()

    def add(self, child, i):
        self.get_root().add(child, i)

    def remove(self, q_index):
        """
        :type q_index: QModelIndex
        """
        node_to_remove = q_index.internalPointer()
        """:type q_index: TreeNode"""
        if node_to_remove:
            parent_q_index = self.__model.parent(q_index)
            parent_node = node_to_remove.parent_node
            """:type :TreeNode"""
            index = node_to_remove.get_row()
            self.__model.beginRemoveRows(parent_q_index, index, index)
            if parent_node:
                parent_node.remove(node_to_remove.get_row())
            self.__model.endRemoveRows()

    def rename(self, new_name, *indexes):
        tree_node = self.get_node(*indexes)
        tree_node.leaf.name = new_name
        return tree_node

    def get_model(self):
        return self.__model

    def set_expanded(self, has_expanded, *indexes):
        self.get_node(*indexes).__is_expanded = has_expanded

    def __getitem__(self, i):
        return self.get_root()[i]

    def get_hotkey(self, *indexes):
        node = self.get_node(*indexes)
        if node.leaf.NAME == Action.NAME:
            return node.leaf.hotkey

    def set_hotkey(self, hotkey_str, node):
        if node.leaf.NAME == Action.NAME:
            node.leaf.hotkey = hotkey_str

    def get_node(self, *indexes):
        """
        :type indexes:list of int
        :rtype :TreeNode
        """
        target = self.get_root()
        for i in indexes:
            target = target[i]
        return target

    def __to_json(self, o):
        if isinstance(o, TreeNode):
            return o.jsonify()
        raise TypeError(repr(o) + ' is not JSON serializable')

    def __from_json(self, o):
        if '__class__' in o:
            if o['__class__'] == TreeNode.NAME:
                return TreeNode.dejsonify(o)
            elif o['__class__'] == ActionRoot.NAME:
                return ActionRoot.dejsonify(o)
            elif o['__class__'] == ActionGroup.NAME:
                return ActionGroup.dejsonify(o)
            elif o['__class__'] == Action.NAME:
                return Action.dejsonify(o)
            elif o['__class__'] == StepItem.NAME:
                return StepItem.dejsonify(o)
        return o

    def save(self):
        print("save")
        with open(Options.steps_path + "action_root.json", "w") as f:
            json.dump(self.get_root(), f, default=self.__to_json, indent=2)

    def load(self):
        try:
            with open(Options.steps_path + "action_root.json", "r") as f:
                loaded_root = json.load(f, object_hook=self.__from_json)
                """:type :TreeNode"""
                self.__model.root_node = loaded_root
        except IOError as exc:
            if exc.errno == errno.ENOENT:
                self.save()
            elif exc.errno != errno.ENOENT:
                raise exc
