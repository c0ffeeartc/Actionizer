__author__ = 'cfe'


class ConditionCollection(object):
    # NOTE: not finished. Delete it?
    def __init__(self, *args):
        self.conditions = []
        for arg in args:
            if arg.typename == "condition":
                self.conditions.append(arg)

    def evaluate(self):
        result = False

        for condition in self.conditions:
            condition.evaluate()

        return result



