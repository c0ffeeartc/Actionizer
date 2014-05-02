__author__ = 'cfe'


class StepItemVO(object):
    """
    StepItem has Step from Pool, its arguments, and links to results from previous steps.
    """
    step = None
    args = {}
    result_links = {}  # i:[key1, key2, etc]

    def __dict__(self):
        return {
            self.step.uid,
            self.args,
            self.result_links,
        }
