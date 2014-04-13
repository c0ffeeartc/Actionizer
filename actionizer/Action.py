__author__ = 'cfe'
import win32com.client


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
            if arg.type_name == "step":
                self.steps.append(arg)
            if arg.type_name == "stepCollection":
                self.steps.append(arg)

    def metPreConditions(self):  # not done
        if "activeDocument" in self.preConditions:
            # check activeDocument
            pass
        return True

    def play(self):

        psApp = win32com.client.Dispatch('Photoshop.Application')

        for step in self.steps:
            step.play(psApp)
