from model.stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.facade import Facade

__author__ = 'cfe'
import win32com.client

STEP_ARGS = "STEP_ARGS"
STEP_UID = "STEP_UID"
STEP = "STEP"


class Action(object):
    """
    Action is step container
    """

    def __init__(self):
        self.name = ""
        self.steps = []
        self.results = []

    def add_step(self, step_uid, i=None):
        if not i:
            i = len(self.steps)
        elif i < 0:
            i = 0
        elif i > len(self.steps):
            i = len(self.steps)

        step_args = {}
        step_pool_proxy = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME)
        step = step_pool_proxy.get_step(step_uid)
        self.steps.insert(i, {STEP: step, STEP_ARGS: step_args})

    def remove_step(self, i):
        if len(self.steps) > i >= 0:
            self.steps.pop(i)

    def replace_step(self, step_uid, i):
        if self.steps[i]:
            self.remove_step(i)
            self.add_step(step_uid, i)

    def set_args(self, args, i):
        if args is dict:
            self.steps[i][STEP_ARGS] = args

    def move_step(self, from_i, to_i):
        if to_i < len(self.steps) and from_i <= len(self.steps):
            self.steps.insert(to_i, self.steps.pop(from_i))

    def move_step_up(self, i):
        last = len(self.steps) - 1
        if last >= i > 0:
            self.move_step(i, i-1)

    def move_step_down(self, i):
        last = len(self.steps) - 1
        if last > i >= 0:
            self.move_step(i, i+1)

    def play(self, start_i=0):
        del self.results[:]
        ps_app = win32com.client.Dispatch('Photoshop.Application')
        for i in xrange(len(self.steps)):
            if i < start_i:
                continue
            result = self.steps[i][STEP].play(ps_app, self.steps[i][STEP_ARGS])
            self.results.append(result)
        del self.results[:]
