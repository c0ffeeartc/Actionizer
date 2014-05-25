__author__ = 'cfe'


class Notes(object):
    STARTUP_COMMAND = "STARTUP_COMMAND"
    START_LISTEN_GLOBAL_HOTKEYS = "START_LISTEN_GLOBAL_HOTKEYS"
    STOP_LISTEN_GLOBAL_HOTKEYS = "STOP_LISTEN_GLOBAL_HOTKEYS"
    SHOW_CONTEXT_MENU = "SHOW_CONTEXT_MENU"
    TREE_MODEL_CHANGED = "TREE_MODEL_CHANGED"
    TREE_NODE_RENAMED = "TREE_NODE_RENAMED"
    TREE_MODEL_ADD = "TREE_MODEL_ADD"
    TREE_MODEL_ADDED = "TREE_MODEL_ADDED"
    TREE_MODEL_REMOVE = "TREE_MODEL_REMOVE"
    TREE_MODEL_REMOVED = "TREE_MODEL_REMOVED"
    TREE_MODEL_SAVE = "TREE_MODEL_SAVE"
    TREE_MODEL_LOAD = "TREE_MODEL_LOAD"
    TREE_MODEL_SAVED = "TREE_MODEL_SAVED"
    TREE_MODEL_LOADED = "TREE_MODEL_LOADED"
    SHOW_RENAME_DIALOG = "SHOW_RENAME_DIALOG"
    SHOW_TEXT_DIALOG = "SHOW_TEXT_DIALOG"
    SHOW_REPLACE_STEP_DIALOG = "SHOW_REPLACE_STEP_DIALOG"
    CONTEXT_MENU_RENAME = "CONTEXT_MENU_RENAME"
    CONTEXT_MENU_REPLACE_STEP = "CONTEXT_MENU_REPLACE_STEP"


class TreeNodeRenamedVO(object):
    def __init__(self, new_name="", indexes=None):
        if not indexes:
            indexes = []
        self.new_name = new_name
        """:type :str"""
        self.indexes = indexes
        """:type :list of int"""


class ShowRenameDialogVO(object):
    def __init__(self, current_name=""):
        self.current_name = current_name
        """:type :str"""


class ShowContextMenuVO(object):
    def __init__(self, parent_widget=None, selected_item=None):
        self.parent_widget = parent_widget
        """:type :QTreeWidgetItem"""
        self.selected_item = selected_item
        """:type :QTreeWidgetItem"""
