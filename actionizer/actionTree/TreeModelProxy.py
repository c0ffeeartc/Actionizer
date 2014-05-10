from actionTree.model.ActionRoot import ActionRoot
from puremvc.patterns.proxy import Proxy

__author__ = 'cfe'


class TreeModelProxy(Proxy):
    NAME = "TreeModelProxy"

    def __init__(self):
        super(TreeModelProxy, self).__init__()
        action_root = ActionRoot()
        action_root.load()
        self.setData(action_root)
