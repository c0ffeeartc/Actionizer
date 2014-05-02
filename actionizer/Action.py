__author__ = 'cfe'
import win32com.client

# TODO: make action manage step argument calls and return results
class Action(object):
    """
    Action is step container
    """

    def __init__(self):
        self.name = ""
        self.steps = []
        self.args = []
        self.results = []

    def add(self, *args):
        for arg in args:
            if arg.type_name == "step":
                self.steps.append(arg)
                self.args.append({})

    def setArgs(self, i, args):
        if args is dict:
            self.args[i] = args

    def play(self, start_index=0):
        ps_app = win32com.client.Dispatch('Photoshop.Application')
        for i in xrange(len(self.steps)):
            if i < start_index:
                continue
            result = self.steps[i].play(ps_app, self.args[i])
            self.results.append(result)
