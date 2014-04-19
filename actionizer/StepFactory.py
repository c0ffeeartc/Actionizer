from Step import Step

__author__ = 'cfe'


class StepUids(object):
    NULL_STEP = "NULL_STEP"
    TEST_STEP = "TEST_STEP"


class StepFactory(object):
    @staticmethod
    def new_step(step_uid):
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
        else:
            print("StepFactory.new_step no step with such uid")
            return StepFactory.new_step(StepUids.NULL_STEP)
