from treedataleaf.Action import Action
from treemdl.model.treenode import TreeNode

__author__ = 'c0ffee'


class HotkeyList(object):
    """
    Keeps in sync list of elements with hotkeys.
    """
    def __init__(self):
        self.hotkey_actions = {}

    def add_hotkey(self, hotkey, action_node):
        if hotkey in self.hotkey_actions.keys() and \
                action_node is not self.hotkey_actions[hotkey]:
            self.hotkey_actions[hotkey].leaf.hotkey = ""
            self.remove_action(self.hotkey_actions[hotkey])
        self.remove_action(action_node)
        if hotkey != "":
            self.hotkey_actions[hotkey] = action_node

    def remove_hotkey(self, hotkey):
        if hotkey in self.hotkey_actions.keys():
            del self.hotkey_actions[hotkey]

    def remove_action(self, action_node):
        for hotkey, stored_action in self.hotkey_actions.items():
            if action_node is stored_action:
                self.remove_hotkey(hotkey)

    def update(self, node):
        """:type node:TreeNode"""
        for child_node in node.child_nodes:
            if child_node.leaf.NAME == Action.NAME and child_node.leaf.hotkey:
                self.hotkey_actions[child_node.leaf.hotkey] = child_node
            if len(child_node.child_nodes):
                self.update(child_node)
