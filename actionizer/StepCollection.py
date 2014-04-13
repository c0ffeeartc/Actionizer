from Condition import Condition

__author__ = 'cfe'


class StepCollection(object):
    """
    Named step container with optional conditional statement
    """

    def __init__(self, *args):
        self.type_name = "stepCollection"
        self.name = ""
        self.steps = []

        # condition = [[a,op,b],]
        self.condition = Condition(None, "do", None)

        for arg in args:
            if arg.type_name == "step":
                self.steps.append(arg)

    def add(self, *args):
        for arg in args:
            if arg.type_name == "step":
                self.steps.append(arg)
            if arg.type_name == "stepCollection":
                self.steps.append(arg)

    def play(self, psApp):
        # plays steps if condition true
        if self.condition.evaluate():
            for step in self.steps:
                step.play(psApp)
