from puremvc.patterns.command import SimpleCommand
from treedataleaf.actiongroup import ActionGroup
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
        root = tree_model_proxy.get_root()
        root.add(TreeNode(ActionGroup()), 0)
        return
        tree_view_mediator = self.facade.retrieveMediator(TreeView2Mediator.NAME)
        """:type :TreeView2Mediator"""

        cur_item = tree_view_mediator.get_cur_item()
        indexes = []

        if cur_item is None:
            tree_model_proxy.add(cur_item, 0)
            return

        is_action = cur_item.text(1) == Action.NAME
        is_group = cur_item.text(1) == ActionGroup.NAME
        is_expanded = cur_item.isExpanded()
        indexes = tree_view_mediator.get_indexes(cur_item)
        child = None

        if is_action and is_expanded:
            child = TreeNode(StepItem())
            """:type :TreeNode"""
            indexes.append(cur_item.childCount())

        elif is_action and not is_expanded:
            child = TreeNode(Action())
            """:type :TreeNode"""
            indexes.append(indexes.pop()+1)

        elif is_group and is_expanded:
            child = TreeNode(Action())
            """:type :TreeNode"""
            indexes.append(cur_item.childCount())

        elif is_group and not is_expanded:
            child = TreeNode(ActionGroup())
            """:type :TreeNode"""
            indexes.append(indexes.pop()+1)

        if child:
            tree_model_proxy.add(child, *indexes)
