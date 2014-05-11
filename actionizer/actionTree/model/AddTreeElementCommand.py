from notifications import Notes
from puremvc.patterns.command import SimpleCommand
from puremvc.patterns.facade import Facade

__author__ = 'cfe'


class AddTreeElementCommand(SimpleCommand):
    NAME = "AddTreeElementCommand"
    def execute(self, note):
        """
        Accepts
        note.body = {
            "index_path":[i,j,k,etc], # depth index
            "element": obj,
        }
        """
        index_path = note.body["index_path"]
        element = note.body["element"]

        # put element into tree
        Facade.getInstance().sendNotification(Notes.TREE_MODEL_ADD)
