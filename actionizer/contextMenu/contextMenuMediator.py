from PySide.QtGui import QCursor
from contextMenu.StepContextMenu import StepContextMenu
from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator

__author__ = 'cfe'


class ContextMenuMediator(Mediator):
    NAME = "ContextMenuMediator"

    def __init__(self):
        super(ContextMenuMediator, self).__init__(self.NAME, StepContextMenu())
        self.__menu = self.viewComponent
        """:type :StepContextMenu"""

    def listNotificationInterests(self):
        return {
            Notes.SHOW_CONTEXT_MENU,
        }

    def handleNotification(self, note):
        if Notes.SHOW_CONTEXT_MENU == note.getName():
            self.__menu.popup(QCursor().pos())

