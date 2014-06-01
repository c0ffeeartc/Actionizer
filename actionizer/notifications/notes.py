__author__ = 'cfe'


class Notes(object):
    STARTUP_COMMAND = "STARTUP_COMMAND"
    START_LISTEN_GLOBAL_HOTKEYS = "START_LISTEN_GLOBAL_HOTKEYS"
    STOP_LISTEN_GLOBAL_HOTKEYS = "STOP_LISTEN_GLOBAL_HOTKEYS"
    PAUSE_LISTEN_GLOBAL_HOTKEYS = "PAUSE_LISTEN_GLOBAL_HOTKEYS"
    UNPAUSE_LISTEN_GLOBAL_HOTKEYS = "UNPAUSE_LISTEN_GLOBAL_HOTKEYS"
    SHOW_CONTEXT_MENU = "SHOW_CONTEXT_MENU"
    TREE_MODEL_CHANGED = "TREE_MODEL_CHANGED"
    TREE_NODE_RENAMED = "TREE_NODE_RENAMED"
    TREE_MODEL_ADD = "TREE_MODEL_ADD"
    TREE_MODEL_ADDED = "TREE_MODEL_ADDED"
    TREE_MODEL_REMOVE = "TREE_MODEL_REMOVE"
    TREE_MODEL_REMOVED = "TREE_MODEL_REMOVED"
    TREE_MODEL_MOVE = "TREE_MODEL_MOVE"
    TREE_MODEL_MOVED = "TREE_MODEL_MOVED"
    TREE_MODEL_SAVE = "TREE_MODEL_SAVE"
    TREE_MODEL_LOAD = "TREE_MODEL_LOAD"
    TREE_MODEL_SAVED = "TREE_MODEL_SAVED"
    TREE_MODEL_LOADED = "TREE_MODEL_LOADED"
    SHOW_RENAME_DIALOG = "SHOW_RENAME_DIALOG"
    SHOW_TEXT_DIALOG = "SHOW_TEXT_DIALOG"
    TREE_MODEL_EXPANDED = "TREE_MODEL_EXPANDED"
    SHOW_REPLACE_STEP_DIALOG = "SHOW_REPLACE_STEP_DIALOG"
    SHOW_HOTKEY_DIALOG = "SHOW_HOTKEY_DIALOG"
    CONTEXT_MENU_RENAME = "CONTEXT_MENU_RENAME"
    CONTEXT_MENU_SET_HOTKEY = "CONTEXT_MENU_SET_HOTKEY"
    CONTEXT_MENU_REPLACE_STEP = "CONTEXT_MENU_REPLACE_STEP"
    REPLACE_STEP_COMMAND = "REPLACE_STEP_COMMAND"
    HOTKEY_CHANGED = "HOTKEY_CHANGED"


class HotkeyChangedVO(object):
    def __init__(self, hotkey_str, indexes):
        """@type hotkey_str:str"""
        self.hotkey_str = hotkey_str
        self.indexes = indexes


class ShowHotkeyDialogVO(object):
    def __init__(self, hotkey):
        """@type hotkey:str"""
        self.hotkey = hotkey


class TreeModelExpandedVO(object):
    def __init__(self, has_expanded, indexes):
        """
        @type has_expanded: bool
        @type indexes: list of int
        @return:
        """
        self.has_expanded = has_expanded
        self.indexes = indexes


class TreeModelMoveVO(object):
    def __init__(self, drag_indexes, target_indexes):
        """
        :type drag_indexes: list of int
        :type target_indexes: list of int
        """
        self.drag_indexes = drag_indexes
        self.target_indexes = target_indexes


class TreeModelMovedVO(TreeModelMoveVO):
    def __init__(self, drag_indexes, target_indexes):
        """
            :type drag_indexes: list of int
            :type target_indexes: list of int
            """
        super(TreeModelMovedVO, self).__init__(drag_indexes, target_indexes)


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


class ReplaceStepCommandVO(object):
    def __init__(self, new_step_uid):
        self.new_step_uid = new_step_uid
