from model.stepPool.StepPool import StepPool
from puremvc.patterns.proxy import Proxy

__author__ = 'c0ffee'


class StepPoolProxy(Proxy):
    NAME = "StepPoolProxy"

    def onRegister(self):
        super(StepPoolProxy, self).onRegister()
        self.setData(StepPool())

    def get_step_pool(self):
        return self.getData()
