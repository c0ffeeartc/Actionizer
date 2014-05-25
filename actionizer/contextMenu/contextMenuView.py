from PySide.QtGui import QMenu, QAction

from stepPool.StepPoolProxy import StepPoolProxy
from notifications.notes import Notes
from puremvc.patterns.facade import Facade


__author__ = 'c0ffee'


class ContextMenuView(QMenu):
    RENAME_ACTION = "&Rename"
    REPLACE_STEP_ACTION = "Replace &Step"

    def __init__(self, *args, **kwargs):
        super(ContextMenuView, self).__init__(*args, **kwargs)
        self.__menu_steps = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME).get_step_files()

        self.__rename = QAction(ContextMenuView.RENAME_ACTION, None)
        # noinspection PyUnresolvedReferences
        self.__rename.triggered.connect(self.on_rename_menu)

        self.__replace_step = QAction(ContextMenuView.REPLACE_STEP_ACTION, None)
        # noinspection PyUnresolvedReferences
        self.__replace_step.triggered.connect(self.on_replace_step)
        self.fill()

    def fill(self):
        self.clear()
        self.addAction(self.__rename)
        self.addAction(self.__replace_step)
        self.addSeparator()
        for step in self.__menu_steps:
            self.addAction(step)

    def on_rename_menu(self):
        Facade.getInstance().sendNotification(Notes.CONTEXT_MENU_RENAME)

    def on_replace_step(self):
        Facade.getInstance().sendNotification(Notes.CONTEXT_MENU_REPLACE_STEP)
