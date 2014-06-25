import win32com.client
from puremvc.patterns.facade import Facade
from stepPool.StepPoolProxy import StepPoolProxy
from stepPool.model.Step import Step

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
        step_pool_proxy = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME)
        """:type :StepPoolProxy"""
        action_script = ""
        for cur_i in xrange(len(step_items)):
            if cur_i < start_i:
                continue
            action_script += Step.py_args_to_javascript_script.encode('string_escape')
            action_script += step_pool_proxy.get_step(step_items[cur_i].leaf.step_uid).script.encode('string_escape')
            action_script += Step.return_script.encode('string_escape')
        self.js_play(ps_app, action_script)
        # Implementation where doJavascript suspendHistory was called on each step
        # for cur_i in xrange(len(step_items)):
        #     if cur_i < start_i:
        #         continue
        #     self.__inject_results(step_items, cur_i)
        #     result = step_items[cur_i].leaf.play(ps_app)
        #     self.results.append(result)
        # del self.results[:]

    def js_play(self, ps_app, action_script):
        ps_source_str = "({})"
        try:

            ps_source_str = ps_app.DoJavaScript(
                "returnStr = {}.toSource();\nif(app.documents.length != 0)\n{app.activeDocument.suspendHistory(\n'" +
                self.name + "', '" + action_script + "'),\n returnStr;}",
                [0],
                1  # PsJavaScriptExecutionMode: 1 (psNeverShowDebugger), 2 (psDebuggerOnError), 3 (psBeforeRunning)
            )

            # except pywintypes.com_error:
            #     ps_app.DoJavaScript("alert('Error in script:" + b + "');")
        finally:
            result_py_dict = Step.py_dict_from_ps_source_str(ps_source_str)
            return result_py_dict

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
