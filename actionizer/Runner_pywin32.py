from StepFactory import StepUids, StepFactory
from model.action.Action import Action

if __name__ == "__main__":
    a_step = StepFactory.new_step(StepUids.TEST_STEP)
    action1 = Action()
    action1.add_step(a_step)
    action1.play()
