from actionTree.model import Action
from stepPool.model.StepFactory import StepUids
from stepPool.model.StepFactory import StepFactory

if __name__ == "__main__":
    a_step = StepFactory.new_step(StepUids.TEST_STEP)
    action1 = Action()
    action1.add_step(a_step)
    action1.play()
