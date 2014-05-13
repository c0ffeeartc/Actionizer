import json
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
        self.root = TreeNode(ActionRoot(), ActionGroup.NAME)
        self.save()

    def play(self, *indexes):
        self.__get_target(*indexes).play()

    def add(self, child, *indexes):
        if indexes:
            i_path = indexes[0:-1]
            i_target = indexes[-1]
            self.__get_target(*i_path).add(child, i_target)
        else:
            self.root.add(child)

    def remove(self, *indexes):
        i_path = indexes[0:-1]
        i_target = indexes[-1]
        return self.__get_target(*i_path).pop(i_target)

    def __getitem__(self, i):
        return self.root[i]

    def __get_target(self, *indexes):
        target = self.root
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
            if o['__class__'] == ActionRoot.NAME:
                return ActionRoot.dejsonify(o)
            if o['__class__'] == Action.NAME:
                return Action.dejsonify(o)
            if o['__class__'] == StepItem.NAME:
                return StepItem.dejsonify(o)
        return o

    def save(self):
        with open(Options.steps_path + "action_root.json", "w") as f:
            json.dump(self.root, f, default=self.__to_json, indent=2)

    def load(self):
        with open(Options.steps_path + "action_root.json", "r") as f:
            self.root.clear()
            self.root = json.load(f, object_hook=self.__from_json)
