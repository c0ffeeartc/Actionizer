import win32com.client
__author__ = 'cfe'


class Action(object):
    """
    Action is step manager and container.
    """
    NAME = "Action"

    def __init__(self):
        self.name = "Action"
        self.results = []
        self.hotkey = ""

    def play(self, step_items, start_i=0):
        """
        Plays steps in action starting from i
        """
        del self.results[:]
        ps_app = win32com.client.Dispatch('Photoshop.Application')
        for cur_i in xrange(len(step_items)):
            if cur_i < start_i:
                continue
            self.__inject_results(step_items, cur_i)
            result = step_items[cur_i].leaf.play(ps_app)
            self.results.append(result)
        del self.results[:]

    def __inject_results(self, step_items, into_step_i):
        """
        Places results from previously played children into arguments of
        step with index
        """
        step_item = step_items[into_step_i]
        for src_i, result_keys in step_item.leaf.result_links.iteritems():
            if src_i > into_step_i:
                continue
            for key in result_keys:
                step_item.step_args[key] = self.results[src_i][key]

    def jsonify(self):
        return {
            "__class__": Action.NAME,
            "__value__": {
                "name": self.name,
                "hotkey": self.hotkey
            }
        }

    @classmethod
    def dejsonify(cls, o):
        if o['__class__'] == Action.NAME:
            action = Action()
            action.name = o["__value__"]["name"]
            action.hotkey = o["__value__"]["hotkey"]
            return action
