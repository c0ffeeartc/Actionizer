from puremvc.patterns.proxy import Proxy

__author__ = 'cfe'


class ActionProxy(Proxy):
    NAME = "ActionProxy"

    def __init__(self):
        super(ActionProxy, self).__init__()
        self.setData(None)

