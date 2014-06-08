import json
import errno

from options.OptionsVO import Options
from treedataleaf.action import Action
from treedataleaf.actiongroup import ActionGroup
from treedataleaf.actionroot import ActionRoot
from treedataleaf.stepitem import StepItem
from treemdl.model.treemodel import TreeModel
from treemdl.model.treenode import TreeNode


__author__ = 'c0ffee'


class TreeManager(object):
    def __init__(self):
        self.model = TreeModel()

    def get_root(self):
        """
        :rtype :TreeNode
        """
        return self.model.root_node

    def play(self, *indexes):
        self.get_node(*indexes).play()

    def add(self, child, i):
        self.get_root().add(child, i)

    def remove(self, *indexes):
        i_parent = indexes[0:-1]
        i_target = indexes[-1]
        return self.get_node(*i_parent).child_nodes.pop(i_target)

    def rename(self, new_name, *indexes):
        tree_node = self.get_node(*indexes)
        tree_node.leaf.name = new_name
        return tree_node

    def get_type(self, *indexes):
        return self.get_node(*indexes).get_type()

    def set_expanded(self, has_expanded, *indexes):
        self.get_node(*indexes).is_expanded = has_expanded

    def __getitem__(self, i):
        return self.get_root()[i]

    def get_hotkey(self, *indexes):
        node = self.get_node(*indexes)
        if node.leaf.NAME == Action.NAME:
            return node.leaf.hotkey

    def set_hotkey(self, hotkey_str, *indexes):
        selected_node = self.get_node(*indexes)
        if selected_node.leaf.NAME == Action.NAME:
            selected_node.leaf.hotkey = hotkey_str

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
                self.model.root_node = loaded_root
                pass
                # for child in loaded_root.children:
                #     self.model.root_node.add(child)
        except IOError as exc:
            if exc.errno == errno.ENOENT:
                self.save()
            elif exc.errno != errno.ENOENT:
                raise exc
