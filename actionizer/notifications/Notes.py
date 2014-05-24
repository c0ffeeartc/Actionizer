from puremvc.patterns.facade import Facade

__author__ = 'cfe'


class Notes(object):
    STARTUP_COMMAND = "STARTUP_COMMAND"
    START_LISTEN_GLOBAL_HOTKEYS = "START_LISTEN_GLOBAL_HOTKEYS"
    STOP_LISTEN_GLOBAL_HOTKEYS = "STOP_LISTEN_GLOBAL_HOTKEYS"
    STEP_CONTEXT_MENU_SELECTED = "STEP_CONTEXT_MENU_SELECTED"
    SHOW_CONTEXT_MENU = "SHOW_CONTEXT_MENU"
    TREE_MODEL_CHANGED = "TREE_MODEL_CHANGED"
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

    @classmethod
    def show_context_menu(cls, parent_widget, selected_item):
        Facade.getInstance().sendNotification(
            Notes.SHOW_CONTEXT_MENU,
            {
                "parent_widget": parent_widget,
                "selected_item": selected_item,
            }
        )