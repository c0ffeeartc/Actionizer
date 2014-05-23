from notifications import Notes
from puremvc.patterns.mediator import Mediator
from textDialog.textDialogView import TextDialog

__author__ = 'cfe'


class TextDialogMediator(Mediator):
    NAME = "TextDialogMediator"
    RENAME_DIALOG = "RENAME_DIALOG"

    def __init__(self):
        self.__dialog = TextDialog()
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
        if TextDialog.TEXT_DIALOG_OK == note.getName():
            if self.__dialog_name == TextDialogMediator.RENAME_DIALOG:
                print(note.getBody()["text"])
            self.__dialog_name = ""
        elif TextDialog.TEXT_DIALOG_CANCEL == note.getName():
            self.__dialog_name = ""
        elif Notes.SHOW_RENAME_DIALOG == note.getName():
            self.__show_rename_dialog(note.getBody()["cur_name"])

    def __dialog(self):
        return self.viewComponent

    def __show_rename_dialog(self, current_name):
        self.__dialog_name = TextDialogMediator.RENAME_DIALOG
        self.__show_text_dialog(current_name)

    def __show_text_dialog(self, text=""):
        self.__dialog.edit_line.setText(text)
        self.__dialog.exec_()
