from actionTree.TreeModelProxy import TreeModelProxy
from actionTree.model.Action import Action
from actionTree.model.ActionGroup import ActionGroup
from actionTree.model.StepItem import StepItem
from actionTree.model.TreeNode import TreeNode
from puremvc.patterns.command import SimpleCommand
from treeView.TreeViewMediator import TreeViewMediator

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
            tree_model_proxy.add(child)
        elif cur_item.text(1) == ActionGroup.NAME:
            cur_item.setExpanded(1)
            child = TreeNode(Action(), StepItem.NAME)
            """:type :TreeNode"""
            indexes = tree_view_mediator.get_indexes(cur_item)
            indexes.append(0)
            tree_model_proxy.add(child, *indexes)
        elif cur_item.text(1) == Action.NAME:
            child = TreeNode(StepItem())
            """:type :TreeNode"""
            print(cur_item.isExpanded())
            cur_item.setExpanded(1)
            print(cur_item.isExpanded())
            indexes = tree_view_mediator.get_indexes(cur_item)
            indexes.append(0)
            tree_model_proxy.add(child, *indexes)