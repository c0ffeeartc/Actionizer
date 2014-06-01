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
            self.facade.sendNotification(Notes.UNPAUSE_LISTEN_GLOBAL_HOTKEYS,)

        elif note.getName() == HotkeyDialogView.HOTKEY_DIALOG_CANCEL:
            self.facade.sendNotification(Notes.UNPAUSE_LISTEN_GLOBAL_HOTKEYS,)

        elif note.getName() == Notes.SHOW_HOTKEY_DIALOG:
            self.facade.sendNotification(Notes.PAUSE_LISTEN_GLOBAL_HOTKEYS,)
            self.__show_hotkey_dialog(note)

    def __show_hotkey_dialog(self, note):
        vo = note.body
        """:type :ShowHotkeyDialogVO"""
        self.__dialog.edit_line.setText(vo.hotkey)
        self.__dialog.exec_()

    def handle_set_hotkey(self, note):
        hotkey_str = note.body["key_sequence"]
        print(hotkey_str)
        tree_mediator = self.facade.retrieveMediator(TreeViewMediator.NAME)
        """:type :TreeViewMediator"""
        indexes = tree_mediator.get_indexes(tree_mediator.get_cur_item())
        tree_proxy = self.facade.retrieveProxy(TreeModelProxy.NAME)
        """:type :TreeModelProxy"""
        tree_proxy.set_hotkey(hotkey_str, *indexes)
