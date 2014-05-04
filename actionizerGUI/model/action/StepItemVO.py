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
