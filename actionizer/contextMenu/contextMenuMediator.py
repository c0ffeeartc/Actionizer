from PySide.QtGui import QCursor
from contextMenu.contextMenuView import ContextMenuView
from notifications.notes import Notes, ShowRenameDialogVO, ShowHotkeyDialogVO
from puremvc.patterns.mediator import Mediator
from treeView.treeViewMediator import TreeViewMediator

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

        if note.name == Notes.SHOW_CONTEXT_MENU:
            tree_mediator = self.facade.retrieveMediator(TreeViewMediator.NAME)
            """:type :TreeViewMediator"""
            item_type = tree_mediator.get_type_name(tree_mediator.get_cur_item())
            self.__menu.fill(item_type)
            self.__menu.popup(QCursor().pos())

        elif note.name == Notes.CONTEXT_MENU_RENAME:
            tree_mediator = self.facade.retrieveMediator(TreeViewMediator.NAME)
            """:type :TreeViewMediator"""
            current_name = tree_mediator.get_cur_item().text(0)
            self.sendNotification(Notes.SHOW_RENAME_DIALOG, ShowRenameDialogVO(current_name))

        elif note.name == Notes.CONTEXT_MENU_REPLACE_STEP:
            self.sendNotification(Notes.SHOW_REPLACE_STEP_DIALOG)

        elif note.name == Notes.CONTEXT_MENU_SET_HOTKEY:
            self.sendNotification(Notes.SHOW_HOTKEY_DIALOG, ShowHotkeyDialogVO(""))
