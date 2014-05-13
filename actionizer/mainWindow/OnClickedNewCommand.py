from actionTree.model.ActionGroup import ActionGroup
from notifications import Notes
from puremvc.patterns.command import SimpleCommand

__author__ = 'cfe'


class OnClickedNewCommand(SimpleCommand):
    NAME = "OnClickedNewCommand"

    def execute(self, note):
        # get tree's current item index
        indexes = note.body["indexes"]
        # i_path = indexes[:-1]
        # i_target = indexes[-1]
        # tree_view_mediator = Facade.getInstance().retrieveMediator(TreeViewMediator.NAME)

        # add new to model
        self.sendNotification(
            Notes.TREE_MODEL_ADD,
            {"child": ActionGroup(), "indexes": [0]},
        )
