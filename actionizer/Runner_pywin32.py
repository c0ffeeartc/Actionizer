from Action import Action
from StepFactory import StepUids, StepFactory

if __name__ == "__main__":
    a_step = StepFactory.new_step(StepUids.TEST_STEP)
    action1 = Action()
    action1.add(a_step)
    action1.play()
