from model.action.ActionRoot import ActionRoot
from puremvc.patterns.proxy import Proxy

__author__ = 'cfe'


class ActionProxy(Proxy):
    NAME = "ActionProxy"

    def __init__(self):
        super(ActionProxy, self).__init__()
        action_root = ActionRoot()
        action_root.load()
        self.setData(action_root)
