from actionTree.model.TypedContainer import TypedContainer
from actionTree.model.Action import Action

__author__ = 'cfe'


class ActionGroup(object):
    """
    Container for actions
    """
    NAME = "ActionGroup"

    def __init__(self):
        self.type_name = ActionGroup.NAME
        self.name = "Action Group"
        self.children = TypedContainer(Action.NAME)

    def jsonify(self):
        return {
            "__class__": self.type_name,
            "__value__":
            {
                "children": self.children.jsonify()
            }
        }

    @classmethod
    def dejsonify(cls, o):
        if o["__class__"] == ActionGroup.NAME:
            action_group = ActionGroup()
            action_group.children = TypedContainer.dejsonify(o["__value__"]["children"])
            return action_group
