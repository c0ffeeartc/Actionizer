import win32com.client

from actionTree.model.StepItemVO import StepItemVO
from actionTree.model.TypedContainer import TypedContainer
from stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.facade import Facade


__author__ = 'cfe'


class Action(object):
    """
    Action is step manager and container.
    """
    NAME = "Action"

    def __init__(self):
        self.name = ""
        self.step_items = TypedContainer(StepItemVO.NAME)
        self.results = []

    def clear(self):
        self.name = ""
        self.step_items.clear()
        del self.results[:]

    def reinit(self, action):
        self.clear()
        if action:
            self.name = action.name
            self.step_items = action.items
            self.results = action.results

    def add_step(self, step_uid, i=None):
        step_pool_proxy = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME)
        item = StepItemVO()
        item.step = step_pool_proxy.get_step(step_uid)
        item.args = {}
        item.result_links = {}
        self.step_items.insert(item, i)

    def remove_step(self, i):
        self.step_items.pop(i)

    def replace_step(self, step_uid, i):
        if self.step_items[i]:
            self.remove_step(i)
            self.add_step(step_uid, i)

    def set_args(self, args, i):
        if args is dict:
            self.step_items[i].args = args

    def move_step(self, from_i, to_i):
        if to_i < len(self.step_items) and from_i <= len(self.step_items):
            self.step_items.insert(to_i, self.step_items.pop(from_i))

    def move_step_up(self, i):
        last = len(self.step_items) - 1
        if last >= i > 0:
            self.move_step(i, i - 1)

    def move_step_down(self, i):
        last = len(self.step_items) - 1
        if last > i >= 0:
            self.move_step(i, i + 1)

    def play(self, start_i=0):
        del self.results[:]
        ps_app = win32com.client.Dispatch('Photoshop.Application')
        for cur_i in xrange(len(self.step_items)):
            if cur_i < start_i:
                continue
            self.__inject_results(cur_i)
            result = self.step_items[cur_i].step.play(ps_app, self.step_items[cur_i].args)
            self.results.append(result)
        del self.results[:]

    def __inject_results(self, into_step_i):
        """
        Places results from previously played step_items into arguments of step with index
        """
        step_item = self.step_items[into_step_i]
        for src_i, result_keys in step_item.result_links.iteritems():
            if src_i > into_step_i:
                continue
            for key in result_keys:
                step_item.step_args[key] = self.results[src_i][key]

    def jsonify(self):
        return {
            "__class__": "Action",
            "__value__":
            {
                "name": self.name,
                "step_items": self.step_items.jsonify(),
                "results": self.results,
            }
        }

    @classmethod
    def dejsonify(cls, o):
        if o['__class__'] == Action.NAME:
            action = Action()
            action.name = o["__value__"]["name"]
            action.step_items = [StepItemVO.dejsonify(step_item) for step_item in o["__value__"]["step_items"]]
            action.results = o["__value__"]["results"]
            return action
