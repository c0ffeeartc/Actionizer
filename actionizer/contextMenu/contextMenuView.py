from PySide.QtGui import QMenu, QAction

from stepPool.StepPoolProxy import StepPoolProxy
from notifications.notes import Notes
from puremvc.patterns.facade import Facade


__author__ = 'c0ffee'


class ContextMenuView(QMenu):
    RENAME_ACTION = "&Rename"

    def __init__(self, *args, **kwargs):
        super(ContextMenuView, self).__init__(*args, **kwargs)
        self.__menu_steps = Facade.getInstance().retrieveProxy(
            StepPoolProxy.NAME).get_step_files()
        self.__rename = QAction(ContextMenuView.RENAME_ACTION, None)
        # noinspection PyUnresolvedReferences
        self.__rename.triggered.connect(self.on_rename_menu)
        self.fill()

    def fill(self):
        self.clear()
        self.addAction(self.__rename)
        self.addSeparator()
        for step in self.__menu_steps:
            self.addAction(step)

    def on_rename_menu(self):
        Notes.show_rename_dialog("name")
