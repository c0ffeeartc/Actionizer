__author__ = 'cfe'


class ActionRoot(object):
    """
    """
    NAME = "ActionRoot"

    def __init__(self):
        pass

    def jsonify(self):
        return {
            "__class__": ActionRoot.NAME,
        }

    @classmethod
    def dejsonify(cls, json_root):
        if json_root["__class__"] == ActionRoot.NAME:
            action_root = ActionRoot()
            return action_root
