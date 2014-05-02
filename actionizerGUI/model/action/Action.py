from model.action.StepItemVO import StepItemVO
from model.stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.facade import Facade

__author__ = 'cfe'
import win32com.client

STEP_ARGS = "STEP_ARGS"
STEP_UID = "STEP_UID"
STEP = "STEP"
RESULT_LINKS = "RESULT_LINKS"


class Action(object):
    """
    Action is step manager and container.
    """

    def __init__(self):
        self.name = ""
        self.results = []
        self.items = []  # StepItems

    def add_step(self, step_uid, i=None):
        if not i:
            i = len(self.items)
        elif i < 0:
            i = 0
        elif i > len(self.items):
            i = len(self.items)

        step_pool_proxy = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME)
        item = StepItemVO()
        item.step = step_pool_proxy.get_step(step_uid)
        item.args = {}
        item.result_links = {}
        self.items.insert(i, item)

    def remove_step(self, i):
        if len(self.items) > i >= 0:
            self.items.pop(i)

    def replace_step(self, step_uid, i):
        if self.items[i]:
            self.remove_step(i)
            self.add_step(step_uid, i)

    def set_args(self, args, i):
        if args is dict:
            self.items[i].args = args

    def move_step(self, from_i, to_i):
        if to_i < len(self.items) and from_i <= len(self.items):
            self.items.insert(to_i, self.items.pop(from_i))

    def move_step_up(self, i):
        last = len(self.items) - 1
        if last >= i > 0:
            self.move_step(i, i - 1)

    def move_step_down(self, i):
        last = len(self.items) - 1
        if last > i >= 0:
            self.move_step(i, i + 1)

    def play(self, start_i=0):
        del self.results[:]
        ps_app = win32com.client.Dispatch('Photoshop.Application')
        for cur_i in xrange(len(self.items)):
            if cur_i < start_i:
                continue
            self.__inject_results(cur_i)
            result = self.items[cur_i].step.play(ps_app, self.items[cur_i].args)
            self.results.append(result)
        del self.results[:]

    def __inject_results(self, into_step_i):
        """
        Places results from previously played items into arguments of step with index
        """
        step_item = self.items[into_step_i]
        for src_i, result_keys in step_item.result_links.iteritems():
            if src_i > into_step_i:
                continue
            for key in result_keys:
                step_item.step_args[key] = self.results[src_i][key]
