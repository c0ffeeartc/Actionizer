from actionTree.TreeModelProxy import TreeModelProxy
from actionTree.model.StepItem import StepItem
from actionTree.model.TreeNode import TreeNode
from puremvc.patterns.command import SimpleCommand
from puremvc.patterns.facade import Facade
from treeView.treeViewMediator import TreeViewMediator

__author__ = 'cfe'


class ReplaceStepCommand(SimpleCommand):
    def execute(self, note):

        tree_mediator = self.facade.retrieveMediator(TreeViewMediator.NAME)
        """:type :TreeViewMediator"""
        tree_proxy = Facade.getInstance().retrieveProxy(TreeModelProxy.NAME)
        """:type :TreeModelProxy"""

        cur_item = tree_mediator.get_cur_item()
        if not StepItem.NAME == \
                tree_mediator.get_type_name(cur_item):
            return

        vo = note.body
        """:type :ReplaceStepCommandVO"""
        step_item = StepItem()
        step_item.step_uid = vo.new_step_uid
        new_node = TreeNode(step_item)
        new_node.leaf.name = vo.new_step_uid
        indexes = tree_mediator.get_indexes(cur_item)
        tree_proxy.replace(new_node, *indexes)
