from actionTree.TreeModelProxy import TreeModelProxy
from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator
from textDialog.textDialogView import TextDialog
from treeView.treeViewMediator import TreeViewMediator

__author__ = 'cfe'


class TextDialogMediator(Mediator):
    NAME = "TextDialogMediator"
    RENAME_DIALOG = "RENAME_DIALOG"
    TEXT_DIALOG = "TEXT_DIALOG"

    def __init__(self):
        self.__dialog = TextDialog()
        super(TextDialogMediator, self).__init__(TextDialogMediator.NAME,
                                                 self.__dialog)
        self.__dialog_name = ""  # used to distinguish currently showed dialog
        self.__dialog = self.viewComponent

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
                self.handle_rename(note)
            self.__dialog_name = ""

        elif note.getName() == TextDialog.TEXT_DIALOG_CANCEL:
            self.__dialog_name = ""

        elif note.getName() == Notes.SHOW_TEXT_DIALOG:
            self.__dialog_name = TextDialogMediator.TEXT_DIALOG
            self.__show_text_dialog(note.getBody()["text"])

        elif note.getName() == Notes.SHOW_RENAME_DIALOG:
            self.__dialog_name = TextDialogMediator.RENAME_DIALOG
            self.__show_text_dialog(note.getBody()["text"])

    def __show_text_dialog(self, text=""):
        self.__dialog.edit_line.setText(text)
        self.__dialog.exec_()

    def handle_rename(self, note):
        new_name = note.getBody()["text"]
        tree_mediator = self.facade.retrieveMediator(TreeViewMediator.NAME)
        """:type :TreeViewMediator"""
        indexes = tree_mediator.get_indexes(tree_mediator.get_cur_item())
        tree_proxy = self.facade.retrieveProxy(TreeModelProxy.NAME)
        """:type :TreeModelProxy"""
        tree_proxy.rename(new_name, *indexes)
