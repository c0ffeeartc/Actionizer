import json, errno
from actionTree.model.Action import Action
from actionTree.model.ActionGroup import ActionGroup
from actionTree.model.ActionRoot import ActionRoot
from actionTree.model.StepItem import StepItem
from actionTree.model.TreeNode import TreeNode
from options.OptionsVO import Options

__author__ = 'cfe'


class TreeManager(object):
    """
    Provides unified interface for tree nodes
    """
    def __init__(self):
        self.root_node = TreeNode(ActionRoot(), ActionGroup.NAME)

    def play(self, *indexes):
        self.__get_target(*indexes).play()

    def add(self, child, *indexes):
        if indexes:
            i_parent = indexes[0:-1]
            i_child = indexes[-1]
            self.__get_target(*i_parent).add(child, i_child)
        else:
            self.root_node.add(child)

    def remove(self, *indexes):
        i_parent = indexes[0:-1]
        i_target = indexes[-1]
        return self.__get_target(*i_parent).children.pop(i_target)

    def rename(self, new_name, *indexes):
        tree_node = self.__get_target(*indexes)
        tree_node.leaf.name = new_name
        return tree_node

    def get_indexes(self, tree_node):
        """
        :type tree_node:TreeNode
        :rtype :list of int
        """
        return tree_node.get_indexes()

    def move(self, from_indexes, to_indexes):
        """
        @param :type from_indexes: list of int
        @param :type to_indexes: list of int
        @return:
        """

        drag_type = self.get_type(*from_indexes)
        target_type = self.get_type(*to_indexes)

        is_step = drag_type == StepItem.NAME
        is_action = drag_type == Action.NAME
        is_group = drag_type == ActionGroup.NAME

        to_step = target_type == StepItem.NAME
        to_action = target_type == Action.NAME
        to_group = target_type == ActionGroup.NAME

        if is_action and to_group or \
                is_step and to_action:
            to_indexes.append(0)
            removed_node = self.remove(*from_indexes)
            self.add(removed_node, *to_indexes)
            return from_indexes, to_indexes

        elif is_group and to_group or \
                is_action and to_action or \
                is_step and to_step:
            removed_node = self.remove(*from_indexes)
            self.add(removed_node, *to_indexes)
            return from_indexes, to_indexes

        return None, None

    def get_type(self, *indexes):
        return self.__get_target(*indexes).get_type()

    def __getitem__(self, i):
        return self.root_node[i]

    def __get_target(self, *indexes):
        """
        :type indexes:list of int
        :rtype :TreeNode
        """
        target = self.root_node
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
            json.dump(self.root_node, f, default=self.__to_json, indent=2)

    def load(self):
        try:
            with open(Options.steps_path + "action_root.json", "r") as f:
                self.root_node.clear()
                self.root_node = json.load(f, object_hook=self.__from_json)
        except IOError as exc:
            if exc.errno == errno.ENOENT:
                self.save()
            elif exc.errno != errno.ENOENT:
                raise exc
