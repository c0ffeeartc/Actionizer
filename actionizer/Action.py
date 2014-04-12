__author__ = 'cfe'


class Action(object):
    """
    Action is step container
    """

    def __init__(self):
        self.name = ""
        self.steps = []
        self.preConditions = []

    def __repr__(self):
        reprStr = ""
        for step in self.steps:
            reprStr += repr(step)
        return reprStr

    def removeStepByIndex(self, index):
        pass

    def add(self, *args):
        for arg in args:
            if arg.typename == "step":
                self.steps.append(arg)
            if arg.typename == "stepCollection":
                self.steps.append(arg)

    def metPreConditions(self):  # not done
        if "activeDocument" in self.preConditions:
            # check activeDocument
            pass
        return True

    def play(self):
        import win32com.client

        psApp = win32com.client.Dispatch('Photoshop.Application')

        for step in self.steps:
            step.play(psApp)
