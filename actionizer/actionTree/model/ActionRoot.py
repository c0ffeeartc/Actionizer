import json

from model.actionTree.ActionGroup import ActionGroup
from model.actionTree.model.vo import TypedContainer


__author__ = 'cfe'


class ActionRoot(object):
    """
    Container for actionGroups
    Should be loaded on start and saved on change and exit.
    """
    NAME = "ActionRoot"

    def __init__(self):
        self.groups = TypedContainer(ActionGroup.NAME)

    def clear(self):
        self.groups.clear()

    def reinit(self, action_root):
        self.clear()
        self.groups = action_root.groups

    def add(self, group, i=None):
        self.groups.insert(group, i)

    def pop(self, i):
        return self.groups.pop(i)

    def jsonify(self):
        return {
            "__class__": ActionRoot.NAME,
            "__value__":
            {
                "groups": self.groups.jsonify()
            }
        }

    @classmethod
    def dejsonify(cls, json_root):
        if json_root["__class__"] == ActionRoot.NAME:
            action_root = ActionRoot()
            action_root.groups = ActionGroup.dejsonify(json_root["__value__"]["groups"])
            return action_root

    def __to_json(self, o):
        if isinstance(o, ActionRoot):
            return o.jsonify()
        raise TypeError(repr(o) + ' is not JSON serializable')

    def __from_json(self, o):
        if '__class__' in o:
            if o['__class__'] == ActionRoot.NAME:
                return self.dejsonify(o)
        return o

    def save(self):
        with open("../../scripts/action_root.json", "w") as f:
            json.dump(self, f, default=self.__to_json, indent=2)

    def load(self):
        with open("../../scripts/action_root.json", "r") as f:
            a_root = json.load(f, object_hook=self.__from_json)
            self.reinit(a_root)
