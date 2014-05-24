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
            Notes.CONTEXT_MENU_SELECTED,
        ]

    def handleNotification(self, note):
        if Notes.SHOW_CONTEXT_MENU == note.getName():
            self.__menu.popup(QCursor().pos())
        elif Notes.CONTEXT_MENU_SELECTED == note.name:
            self.handle_selected(note)

    def handle_selected(self, note):
        print(note.body["txt"])
        # replaces step
        # step_uid = note.body["txt"]
        # tree = self.get_main_window().tree
        # old_item = tree.currentItem()
        # item_parent = old_item.parent()
        # old_item_index = old_item.parent().indexOfChild(old_item)
        # item_parent.removeChild(old_item)
        # self.get_main_window().add_step(step_uid, item_parent,
        #  old_item_index)
