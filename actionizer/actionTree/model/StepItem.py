from stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.facade import Facade

__author__ = 'cfe'


class StepItem(object):
    """
    StepItem has Step from Pool, its arguments, and links to results from previous steps.
    """
    NAME = "StepItem"

    def __init__(self):
        self.step_uid = None
        self.name = ""
        self.args = {}
        self.result_links = {}  # i:[key1, key2, etc]

    def play(self, ps_app):
        step_pool_proxy = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME)
        step = step_pool_proxy.get_step(self.step_uid)
        return step.play(ps_app, self.args)

    def jsonify(self):
        return {
            "__class__": StepItem.NAME,
            "__value__":
            {
                "name": self.name,
                "script_path_name": self.step_uid,
                "args": self.args,
                "result_links": self.result_links,
            },
        }

    @classmethod
    def dejsonify(cls, json_item):
        if json_item["__class__"] == StepItem.NAME:
            step_item = StepItem()
            if "name" in json_item["__value__"].keys():
                step_item.name = json_item["__value__"]["name"]
            step_item.step_uid = json_item["__value__"]["script_path_name"]
            step_item.args = json_item["__value__"]["args"]
            step_item.result_links = json_item["__value__"]["result_links"]
            return step_item
