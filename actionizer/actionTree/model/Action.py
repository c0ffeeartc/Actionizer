import win32com.client

from actionTree.model.StepItem import StepItem
from actionTree.model.TypedContainer import TypedContainer

__author__ = 'cfe'


class Action(object):
    """
    Action is step manager and container.
    """
    NAME = "Action"

    def __init__(self):
        self.type_name = Action.NAME
        self.name = ""
        self.results = []
        self.children = TypedContainer(StepItem.NAME)

    def __getitem__(self, i):
        return self.children[i]

    def set_args(self, args, i):
        if args is dict:
            self.children[i].args = args

    def play(self, start_i=0):
        del self.results[:]
        ps_app = win32com.client.Dispatch('Photoshop.Application')
        for cur_i in xrange(len(self.children)):
            if cur_i < start_i:
                continue
            self.__inject_results(cur_i)
            result = self.children[cur_i].step.play(ps_app, self.children[cur_i].args)
            self.results.append(result)
        del self.results[:]

    def __inject_results(self, into_step_i):
        """
        Places results from previously played children into arguments of step with index
        """
        step_item = self.children[into_step_i]
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
                "children": self.children.jsonify(),
                "results": self.results,
            }
        }

    @classmethod
    def dejsonify(cls, o):
        if o['__class__'] == Action.NAME:
            action = Action()
            action.name = o["__value__"]["name"]
            action.children = [StepItem.dejsonify(step_item) for step_item in o["__value__"]["children"]]
            action.results = o["__value__"]["results"]
            return action
