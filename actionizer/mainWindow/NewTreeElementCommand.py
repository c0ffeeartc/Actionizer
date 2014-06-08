from puremvc.patterns.command import SimpleCommand
from treedataleaf.action import Action
from treedataleaf.actiongroup import ActionGroup
from treedataleaf.stepitem import StepItem
from treedataleaf.ui import UI
from treemdl.model.treenode import TreeNode
from treemdl.treemodel2proxy import TreeModel2Proxy
from treeview2.treeview2mediator import TreeView2Mediator

__author__ = 'cfe'


class NewTreeElementCommand(SimpleCommand):
    """
    """
    NAME = "NewTreeElementCommand"

    def execute(self, note):
        tree_model_proxy = self.facade.retrieveProxy(TreeModel2Proxy.NAME)
        """:type :TreeModel2Proxy"""
        tree_view_mediator = self.facade.retrieveMediator(TreeView2Mediator.NAME)
        """:type :TreeView2Mediator"""

        parent_node = tree_view_mediator.get_cur_item()
        """:type :TreeNode"""
        indexes = []

        if parent_node is None:
            index = 0
            tree_model_proxy.get_root().add(TreeNode(ActionGroup()), index)
            tree_model_proxy.get_model().rowsInserted.emit(parent_node, index, index)
            return
        parent_type = parent_node.get_type()
        is_action = parent_type == UI.ACTION
        is_group = parent_type == UI.ACTION_GROUP
        is_expanded = parent_node.get_is_expanded()

        child = None

        index = len(parent_node.child_nodes)
        if is_action and is_expanded:
            child = TreeNode(StepItem())
            """:type :TreeNode"""

        elif is_action and not is_expanded:
            child = TreeNode(StepItem())
            """:type :TreeNode"""

        elif is_group and is_expanded:
            child = TreeNode(Action())
            """:type :TreeNode"""

        elif is_group and not is_expanded:
            child = TreeNode(Action())
            """:type :TreeNode"""

        if child:
            parent_node.add(child, index)
            tree_model_proxy.get_model().rowsInserted.emit(parent_node, index, index)
