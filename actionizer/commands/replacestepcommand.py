from puremvc.patterns.command import SimpleCommand
from treedataleaf.stepitem import StepItem
from treeview2.treeview2mediator import TreeView2Mediator

__author__ = 'cfe'


class ReplaceStepCommand(SimpleCommand):
    def execute(self, note):

        tree_mediator = self.facade.retrieveMediator(TreeView2Mediator.NAME)
        """:type :TreeView2Mediator"""

        current_node = tree_mediator.get_current_node()
        if not StepItem.NAME == current_node.get_type():
            return

        vo = note.body
        """:type :ReplaceStepCommandVO"""
        current_node.step_uid = vo.new_step_uid
        current_node.rename(vo.new_step_uid)
