from treedataleaf.action import Action

__author__ = 'c0ffee'


class HotkeyList(object):
    def __init__(self):
        self.hotkey_actions = {}

    def add_hotkey(self, hotkey, action_node):
        self.remove_action(action_node)
        self.hotkey_actions[hotkey] = action_node

    def remove_hotkey(self, hotkey):
        if hotkey in self.hotkey_actions.keys():
            del self.hotkey_actions[hotkey]

    def remove_action(self, action_node):
        for hotkey, stored_action in self.hotkey_actions.items():
            if action_node is stored_action:
                self.remove_hotkey(hotkey)

    def update(self, node):
        """:type node:"""
        for child_node in node.child_nodes:
            if child_node.leaf.NAME == Action.NAME and child_node.leaf.hotkey:
                self.hotkey_actions[child_node.leaf.hotkey] = child_node
            if len(child_node.child_nodes):
                self.update(child_node)
