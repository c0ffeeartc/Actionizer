from PySide.QtCore import Qt

from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator
from hotkeydialog.hotkeydialogview import HotkeyDialogView
from treemdl.treemodel2proxy import TreeModel2Proxy
from treeview2.treeview2mediator import TreeView2Mediator


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
        buttons = vo.hotkey.split("+")
        self.__dialog.edit_line.setText(buttons[-1])
        self.__dialog.control_check.setChecked("Ctrl" in buttons)
        self.__dialog.alt_check.setChecked("Alt" in buttons)
        self.__dialog.shift_check.setChecked("Shift" in buttons)
        self.__dialog.exec_()

    def handle_set_hotkey(self, note):
        tree_mediator = self.facade.retrieveMediator(TreeView2Mediator.NAME)
        """:type :TreeView2Mediator"""
        tree_proxy = self.facade.retrieveProxy(TreeModel2Proxy.NAME)
        """:type :TreeModel2Proxy"""
        hotkey_str = note.body["key_sequence"]
        cur_node = tree_mediator.get_current_node()
        tree_proxy.set_hotkey(hotkey_str, cur_node)
