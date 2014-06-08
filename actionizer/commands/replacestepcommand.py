from puremvc.patterns.command import SimpleCommand
from puremvc.patterns.facade import Facade
from treedataleaf.stepitem import StepItem
from treemdl.model.treenode import TreeNode
from treemdl.treemodel2proxy import TreeModel2Proxy
from treeview2.treeview2mediator import TreeView2Mediator

__author__ = 'cfe'


class ReplaceStepCommand(SimpleCommand):
    def execute(self, note):

        tree_mediator = self.facade.retrieveMediator(TreeView2Mediator.NAME)
        """:type :TreeView2Mediator"""
        tree_proxy = Facade.getInstance().retrieveProxy(TreeModel2Proxy.NAME)
        """:type :TreeModel2Proxy"""

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
