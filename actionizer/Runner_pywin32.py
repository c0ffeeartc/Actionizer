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

if __name__ == "__main__":
    builtinStep = get_builtin_step("helloResult")
    astep4 = Step()
    astep4.from_dict(builtinStep)
    stepCol = StepCollection(astep4)
    # stepCol.condition.a = 1
    # stepCol.condition.b = "le"
    # stepCol.condition.op = "le"
    action1 = Action()

    action1.add(stepCol)
    # action1.steps[0].steps[2].setArg("index", 0)

    print ("helloWorld")
    action1.play()
