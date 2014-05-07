from model.actionTree.model.vo import TypedContainer, Action

__author__ = 'cfe'


class ActionGroup(object):
    """
    Container for actions
    """
    NAME = "ActionGroup"

    def __init__(self):
        self.actions = TypedContainer(Action.NAME)

    def clear(self):
        self.actions.clear()

    def add(self, action, i=None):
        self.actions.insert(action, i)

    def jsonify(self):
        return {
            "__class__": ActionGroup.NAME,
            "__value__":
            {
                "actions": self.actions.jsonify()
            }
        }

    @classmethod
    def dejsonify(cls, o):
        if o["__class__"] == ActionGroup.NAME:
            action_group = ActionGroup()
            action_group.actions = TypedContainer.dejsonify(o["__value__"]["actions"])
            return action_group
