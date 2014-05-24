from PySide.QtGui import QCursor
from contextMenu.contextMenuView import ContextMenuView
from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator

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
        ]

    def handleNotification(self, note):
        if Notes.SHOW_CONTEXT_MENU == note.getName():
            self.__menu.popup(QCursor().pos())
