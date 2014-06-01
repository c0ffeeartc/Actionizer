from PySide.QtCore import Qt
from actionTree.TreeModelProxy import TreeModelProxy
from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator
from hotkeydialog.hotkeydialogview import HotkeyDialogView
from treeView.treeViewMediator import TreeViewMediator

__author__ = 'c0ffee'


class HotkeyDialogMediator(Mediator):
    NAME = "HotkeyDialogMediator"

    def __init__(self):
        self.__dialog = HotkeyDialogView(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        super(HotkeyDialogMediator, self).__init__(HotkeyDialogMediator.NAME, self.__dialog)

    def listNotificationInterests(self):
        return [
            Notes.SHOW_HOTKEY_DIALOG,
            HotkeyDialogView.HOTKEY_DIALOG_OK,
            HotkeyDialogView.HOTKEY_DIALOG_CANCEL,
        ]

    def handleNotification(self, note):
        """
        :type note:Notification
        """
        if note.getName() == HotkeyDialogView.HOTKEY_DIALOG_OK:
            self.handle_set_hotkey(note)
        elif note.getName() == HotkeyDialogView.HOTKEY_DIALOG_CANCEL:
            pass
        elif note.getName() == Notes.SHOW_HOTKEY_DIALOG:
            self.__show_hotkey_dialog(note)

    def __show_hotkey_dialog(self, note):
        vo = note.body
        """:type :ShowHotkeyDialogVO"""
        self.__dialog.edit_line.setText(vo.hotkey)
        self.__dialog.exec_()

    def handle_set_hotkey(self, note):
        new_name = note.getBody()["text"]
        tree_mediator = self.facade.retrieveMediator(TreeViewMediator.NAME)
        """:type :TreeViewMediator"""
        indexes = tree_mediator.get_indexes(tree_mediator.get_cur_item())
        tree_proxy = self.facade.retrieveProxy(TreeModelProxy.NAME)
        """:type :TreeModelProxy"""
        # tree_proxy.rename(new_name, *indexes)
