from PySide.QtCore import Qt
from combodialog.combodialogview import ComboDialog
from notifications.notes import Notes, ReplaceStepCommandVO
from puremvc.patterns.mediator import Mediator
from stepPool.StepPoolProxy import StepPoolProxy

__author__ = 'cfe'


class ComboDialogMediator(Mediator):
    NAME = "ComboDialogMediator"

    def __init__(self):
        self.__dialog = ComboDialog(None,
                                    Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        super(ComboDialogMediator, self).__init__(ComboDialogMediator.NAME,
                                                  self.__dialog)

    def listNotificationInterests(self):
        return [
            Notes.SHOW_REPLACE_STEP_DIALOG,
            ComboDialog.COMBO_DIALOG_OK,
            ComboDialog.COMBO_DIALOG_CANCEL,
        ]

    def handleNotification(self, note):

        if note.name == Notes.SHOW_REPLACE_STEP_DIALOG:
            step_pool_proxy = self.facade.retrieveProxy(StepPoolProxy.NAME)
            """:type :StepPoolProxy"""
            self.__dialog.combo_box.clear()
            self.__dialog.combo_box.addItems(step_pool_proxy.get_step_files())
            self.__dialog.exec_()

        elif note.name == ComboDialog.COMBO_DIALOG_OK:
            self.facade.sendNotification(
                Notes.REPLACE_STEP_COMMAND,
                ReplaceStepCommandVO(self.__dialog.combo_box.currentText()))

        elif note.name == ComboDialog.COMBO_DIALOG_CANCEL:
            pass
