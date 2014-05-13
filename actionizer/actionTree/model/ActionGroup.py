__author__ = 'cfe'


class ActionGroup(object):
    NAME = "ActionGroup"

    def __init__(self):
        self.name = "Action Group"

    def jsonify(self):
        return {
            "__class__": ActionGroup.NAME,
            "__value__":
            {
                "name": self.name
            }
        }

    @classmethod
    def dejsonify(cls, o):
        if o["__class__"] == ActionGroup.NAME:
            action_group = ActionGroup()
            action_group.name = o["__value__"]["name"]
            return action_group
