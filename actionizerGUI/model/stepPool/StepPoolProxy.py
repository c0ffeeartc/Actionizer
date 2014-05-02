from Step import Step
from model.stepPool.StepPool import StepPool
from puremvc.patterns.proxy import Proxy

__author__ = 'c0ffee'


class StepPoolProxy(Proxy):
    NAME = "StepPoolProxy"

    def onRegister(self):
        super(StepPoolProxy, self).onRegister()
        self.setData(StepPool())

    def __get_step_pool(self):
        return self.getData()

    def get_step_files(self):
        return self.__get_step_pool().step_files

    def get_step(self, step_uid):
        step = self.__get_step_pool().get_step(script_path_name=step_uid)
        if not step:
            step = Step()
        return step
