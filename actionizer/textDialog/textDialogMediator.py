from PySide.QtCore import Qt

from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator
from textDialog.textDialogView import TextDialog
from treeview2.treeview2mediator import TreeView2Mediator


__author__ = 'cfe'


class TextDialogMediator(Mediator):
    NAME = "TextDialogMediator"
    RENAME_DIALOG = "RENAME_DIALOG"
    TEXT_DIALOG = "TEXT_DIALOG"

    def __init__(self):
        self.__dialog = TextDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        super(TextDialogMediator, self).__init__(TextDialogMediator.NAME,
                                                 self.__dialog)
        self.__dialog_name = ""  # used to distinguish currently showed dialog

    def listNotificationInterests(self):
        return [
            Notes.SHOW_RENAME_DIALOG,
            Notes.SHOW_TEXT_DIALOG,
            TextDialog.TEXT_DIALOG_OK,
            TextDialog.TEXT_DIALOG_CANCEL,
        ]

    def handleNotification(self, note):
        """
        :type note:Notification
        """
        if note.getName() == TextDialog.TEXT_DIALOG_OK:
            if self.__dialog_name == TextDialogMediator.RENAME_DIALOG:
                new_name = note.getBody()["text"]
                tree_mediator = self.facade.retrieveMediator(TreeView2Mediator.NAME)
                """:type :TreeView2Mediator"""
                tree_mediator.get_current_node().rename(new_name)
            self.__dialog_name = ""
            self.facade.sendNotification(Notes.UNPAUSE_LISTEN_GLOBAL_HOTKEYS)

        elif note.getName() == TextDialog.TEXT_DIALOG_CANCEL:
            self.__dialog_name = ""
            self.facade.sendNotification(Notes.UNPAUSE_LISTEN_GLOBAL_HOTKEYS)

        elif note.getName() == Notes.SHOW_TEXT_DIALOG:
            self.__dialog_name = TextDialogMediator.TEXT_DIALOG
            self.__show_text_dialog(note.getBody()["text"])

        elif note.getName() == Notes.SHOW_RENAME_DIALOG:
            vo = note.body
            """:type :ShowRenameDialogVO"""
            self.facade.sendNotification(Notes.PAUSE_LISTEN_GLOBAL_HOTKEYS)
            self.__dialog.setWindowTitle("Rename")
            self.__dialog_name = TextDialogMediator.RENAME_DIALOG
            self.__show_text_dialog(vo.current_name)

    def __show_text_dialog(self, text=""):
        self.__dialog.edit_line.setText(text)
        self.__dialog.exec_()
