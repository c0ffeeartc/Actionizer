from actionTree.TreeModelProxy import TreeModelProxy
from actionTree.model.Action import Action
from actionTree.model.ActionGroup import ActionGroup
from actionTree.model.TreeNode import TreeNode
from puremvc.patterns.command import SimpleCommand
from puremvc.patterns.facade import Facade

__author__ = 'cfe'


class NewTreeElementCommand(SimpleCommand):
    NAME = "NewTreeElementCommand"

    def execute(self, note):
        tree_model_proxy = Facade.getInstance().retrieveProxy(TreeModelProxy.NAME)
        child = TreeNode(ActionGroup(), [Action.NAME])
        indexes = [0]
        tree_model_proxy.add(child, *indexes)
        # child = note.body["child"]
        # indexes = note.body["indexes"]
        # i_path = indexes[:-1]
        # i_target = indexes[-1]

        # add new to model
        # self.sendNotification(
        #     Notes.TREE_MODEL_CH,
        #     {"child": TreeNode(ActionGroup(), [Action.NAME]), "indexes": [0]},
        # )
