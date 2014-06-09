from PySide.QtGui import QCursor
from contextMenu.contextMenuView import ContextMenuView
from notifications.notes import Notes, ShowRenameDialogVO, ShowHotkeyDialogVO
from puremvc.patterns.mediator import Mediator
from treeview2.treeview2mediator import TreeView2Mediator

__author__ = 'cfe'


class ContextMenuMediator(Mediator):
    NAME = "ContextMenuMediator"

    def __init__(self):
        super(ContextMenuMediator, self).__init__(self.NAME, ContextMenuView())
        self.__menu = self.viewComponent
        """:type :ContextMenuView"""

    def listNotificationInterests(self):
        return [
            Notes.SHOW_CONTEXT_MENU,
            Notes.CONTEXT_MENU_RENAME,
            Notes.CONTEXT_MENU_REPLACE_STEP,
            Notes.CONTEXT_MENU_SET_HOTKEY,
        ]

    def handleNotification(self, note):

        tree_mediator = self.facade.retrieveMediator(TreeView2Mediator.NAME)
        """:type :TreeView2Mediator"""
        if note.name == Notes.SHOW_CONTEXT_MENU:
            vo = note.body
            """:type :ShowContextMenuVO"""
            item_type = vo.selected_item.get_type()
            self.__menu.fill(item_type)
            self.__menu.popup(QCursor().pos())

        elif note.name == Notes.CONTEXT_MENU_RENAME:
            """:type :TreeViewMediator"""
            current_name = tree_mediator.get_current_node().get_name()
            self.sendNotification(Notes.SHOW_RENAME_DIALOG, ShowRenameDialogVO(current_name))

        elif note.name == Notes.CONTEXT_MENU_REPLACE_STEP:
            self.sendNotification(Notes.SHOW_REPLACE_STEP_DIALOG)

        elif note.name == Notes.CONTEXT_MENU_SET_HOTKEY:
            self.sendNotification(Notes.SHOW_HOTKEY_DIALOG, ShowHotkeyDialogVO(""))
