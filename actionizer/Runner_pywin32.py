from Action import Action
from Step import Step
from StepCollection import StepCollection
from BuiltinSteps import builtinSteps, get_builtin_step


# Init========================================
# script algorithm
# 1. duplicate to new document
# 2. select upper first Layer
# 3. # insure layerSets are hidden
#    for layerSet in layersSets:
#           hide layerset
#       selectNextLayer
# 4. # save each group to separate file
# iterate layerSets
# turn layerSet visibility on
# save to file
# turn layerSet visibility off

# =============================
# playAction(action)
# =============================
#astep1 = Step(get_builtin_step("newLayer"))
#step = {
#    "uid": "alertStep",
#    "type_name": "step",
#    "script": 'alert(arguments[1]+" :");if (arguments.length>10){alert (arguments[0]);alert (arguments[1])}',
#    "arguments": ["one", astep1.uid, "third"]
#}
from StepFactory import StepUids, StepFactory

if __name__ == "__main__":
    # builtinStep = get_builtin_step("testStep")
    a_step = StepFactory.new_step(StepUids.TEST_STEP)
    # a_step.from_builtin(builtinStep)
    stepCol = StepCollection(a_step)
    # stepCol.condition.a = 1
    # stepCol.condition.b = "le"
    # stepCol.condition.op = "le"
    action1 = Action()

    action1.add(stepCol)
    # action1.steps[0].steps[2].set_arg("index", 0)

    print("helloWorld")
    action1.play()
