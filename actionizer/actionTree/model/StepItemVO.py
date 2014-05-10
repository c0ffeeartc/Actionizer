from stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.facade import Facade

__author__ = 'cfe'


class StepItemVO(object):
    """
    StepItem has Step from Pool, its arguments, and links to results from previous steps.
    """
    NAME = "StepItemVO"

    def __init__(self):
        self.step = None
        self.args = {}
        self.result_links = {}  # i:[key1, key2, etc]

    def jsonify(self):
        return {
            "__class__": StepItemVO.NAME,
            "__value__":
            {
                "script_path_name": self.step.script_path_name,
                "args": self.args,
                "result_links": self.result_links,
            },
        }

    @classmethod
    def dejsonify(cls, json_item):
        if "__class__" == StepItemVO.NAME:
            step_pool_proxy = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME)
            step = step_pool_proxy.get_step(json_item["__value__"]["script_path_name"])
            step_item = StepItemVO()
            step_item.step = step
            step_item.args = json_item["value"]["args"]
            step_item.result_links = json_item["value"]["result_links"]
            return step_item
