import json

from actionTree.model.ActionGroup import ActionGroup
from actionTree.model.TypedContainer import TypedContainer
from options.OptionsVO import Options


__author__ = 'cfe'


class ActionRoot(object):
    """
    Container for actionGroups
    Should be loaded on start and saved on change and exit.
    """
    NAME = "ActionRoot"

    def __init__(self):
        self.type_name = ActionRoot.NAME
        self.children = TypedContainer(ActionGroup.NAME)

    def __getitem__(self, i):
        return self.children[i]

    def jsonify(self):
        return {
            "__class__": ActionRoot.NAME,
            "__value__":
            {
                "children": self.children.jsonify()
            }
        }

    @classmethod
    def dejsonify(cls, json_root):
        if json_root["__class__"] == ActionRoot.NAME:
            action_root = ActionRoot()

            action_root.children = TypedContainer.dejsonify(json_root["__value__"]["children"])
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
        with open(Options.steps_path + "action_root.json", "w") as f:
            json.dump(self, f, default=self.__to_json, indent=2)

    def load(self):
        with open(Options.steps_path + "action_root.json", "r") as f:
            a_root = json.load(f, object_hook=self.__from_json)
            self.children.clear()
            for child in a_root.children:
                self.children.add(child)
