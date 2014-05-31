from actionTree.TreeModelProxy import TreeModelProxy
from actionTree.model.Action import Action
from actionTree.model.ActionGroup import ActionGroup
from actionTree.model.StepItem import StepItem
from actionTree.model.TreeNode import TreeNode
from puremvc.patterns.command import SimpleCommand
from treeView.treeViewMediator import TreeViewMediator

__author__ = 'cfe'


class NewTreeElementCommand(SimpleCommand):
    """
    """
    NAME = "NewTreeElementCommand"

    def execute(self, note):
        tree_view_mediator = self.facade.retrieveMediator(TreeViewMediator.NAME)
        """:type :TreeViewMediator"""
        tree_model_proxy = self.facade.retrieveProxy(TreeModelProxy.NAME)
        """:type :TreeModelProxy"""
        cur_item = tree_view_mediator.get_cur_item()
        indexes = []

        if not cur_item:
            child = TreeNode(ActionGroup(), Action.NAME)
            """:type :TreeNode"""
            indexes.append(0)
            tree_model_proxy.add(child, *indexes)
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
            child = TreeNode(Action(), StepItem.NAME)
            """:type :TreeNode"""
            indexes.append(indexes.pop()+1)

        elif is_group and is_expanded:
            child = TreeNode(Action(), StepItem.NAME)
            """:type :TreeNode"""
            indexes.append(cur_item.childCount())

        elif is_group and not is_expanded:
            child = TreeNode(ActionGroup(), Action.NAME)
            """:type :TreeNode"""
            indexes.append(indexes.pop()+1)

        if child:
            tree_model_proxy.add(child, *indexes)
