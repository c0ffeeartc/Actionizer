from Action import Action
from Step import Step
from StepCollection import StepCollection
from BuiltinSteps import builtinSteps


#def playAction(action):
#    import win32com.client
#    psApp = win32com.client.Dispatch('Photoshop.Application')

#    for step in action:
#        psApp.DoJavaScript(step["script"], step["arguments"])


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
#astep1 = Step(getBuiltinStep("newLayer"))
#step = {
#    "Uid": "alertStep",
#    "typename": "step",
#    "script": 'alert(arguments[1]+" :");if (arguments.length>10){alert (arguments[0]);alert (arguments[1])}',
#    "arguments": ["one", astep1.Uid, "third"]
#}
#astep2 = Step(step)
#astep3 = Step(getBuiltinStep("activateLayerByIndex"))

if __name__ == "__main__":
    print("Hello world")
    # astep4 = Step(getBuiltinStep("helloResult"))

    # stepCol = StepCollection(astep4)
    # stepCol.condition.a = 1
    # stepCol.condition.b = "le"
    # stepCol.condition.op = "le"
    # action1 = Action()

    # action1.add(stepCol)
    #action1.steps[0].steps[2].setArg("index", 0)

    # action1.play()
