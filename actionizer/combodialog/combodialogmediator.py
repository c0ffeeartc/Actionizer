from PySide.QtCore import Qt
from combodialog.combodialogview import ComboDialog
from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator

__author__ = 'cfe'


class ComboDialogMediator(Mediator):
    NAME = "ComboDialogMediator"
    def __init__(self):
        self.__dialog = ComboDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        super(ComboDialogMediator, self).__init__(ComboDialogMediator.NAME, self.__dialog)

    def listNotificationInterests(self):
        return [
                Notes.SHOW_REPLACE_STEP_DIALOG,
                ComboDialog.COMBO_DIALOG_OK,
                ComboDialog.COMBO_DIALOG_CANCEL,
            ]

    def handleNotification(self, note):
        if note.name == Notes.SHOW_REPLACE_STEP_DIALOG:
            self.__dialog.exec_()
        elif note.name == ComboDialog.COMBO_DIALOG_OK:
            print("combo_accepted")
        elif note.name == ComboDialog.COMBO_DIALOG_CANCEL:
            pass
