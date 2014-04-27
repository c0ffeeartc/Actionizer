from Step import Step
from model.stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.facade import Facade

__author__ = 'cfe'


class StepUids(object):
    NULL_STEP = "NULL_STEP"
    TEST_STEP = "TEST_STEP"
    FROM_JSX = "FROM_JSX"


class StepFactory(object):
    @staticmethod
    def new_step(step_uid, **kwargs):
        step = Step()
        step.uid = step_uid
        if step.uid == StepUids.NULL_STEP:
            step.script = "alert ('nullStep');"
            return step
        elif step.uid == StepUids.TEST_STEP:
            step.arg_dict = {
                "isOk": True,
                "numLines": 4,
                "portion": 0.1234567890,
                "portion2": 1,
                "none": None,
                "hello": "HelloWorld",
                "hasReturn": True
            }
            step.script = """
                var step_result = args
                args.hello = "byeBye!!"
                alert ('testStep');
            """
            return step
        elif step.uid == StepUids.FROM_JSX:
            if "file_path_name" in kwargs.keys():
                step_pool = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME).__get_step_pool()
                step = step_pool.get_step(file_path_name=kwargs["file_path_name"])
            return step
        else:
            print("StepFactory.new_step no step with such uid")
            return StepFactory.new_step(StepUids.NULL_STEP)
