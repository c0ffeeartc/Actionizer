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

        parent_node = tree_view_mediator.get_current_node()
        """:type :TreeNode"""
        cur_q_index = tree_view_mediator.get_current_q_index()
        """:type :QModelIndex"""

        if parent_node is None:
            parent_node = tree_model_proxy.get_root()
            child = TreeNode(ActionGroup())
            index = 0
            tree_model_proxy.get_model().beginInsertRows(cur_q_index, index, index)
            parent_node.add(child, index)
            tree_model_proxy.get_model().endInsertRows()
            return

        tree_view_mediator.viewComponent.setExpanded(cur_q_index, True)
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
            tree_model_proxy.get_model().beginInsertRows(cur_q_index, index, index)
            parent_node.add(child, index)
            tree_model_proxy.get_model().endInsertRows()
