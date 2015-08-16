from PySide.QtGui import QMenu, QAction

from stepPool.StepPoolProxy import StepPoolProxy
from notifications.notes import Notes
from puremvc.patterns.facade import Facade
from treedataleaf.UI import UI


__author__ = 'c0ffee'


class ContextMenuView(QMenu):
    RENAME_ACTION = "&Rename"
    REPLACE_STEP_ACTION = "Replace &Step"
    SET_HOTKEY_ACTION = "Set &Hotkey"

    def __init__(self, *args, **kwargs):
        super(ContextMenuView, self).__init__(*args, **kwargs)
        self.__menu_steps = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME).get_step_files()

        self.__rename = QAction(ContextMenuView.RENAME_ACTION, None)
        self.__replace_step = QAction(ContextMenuView.REPLACE_STEP_ACTION, None)
        self.__set_hotkey = QAction(ContextMenuView.SET_HOTKEY_ACTION, None)
        # noinspection PyUnresolvedReferences
        self.__rename.triggered.connect(self.on_rename_menu)
        # noinspection PyUnresolvedReferences
        self.__replace_step.triggered.connect(self.on_replace_step)
        # noinspection PyUnresolvedReferences
        self.__set_hotkey.triggered.connect(self.on_set_hotkey)

        self.fill(None)
        self.addAction(self.__rename)
        self.addAction(self.__replace_step)
        self.addAction(self.__set_hotkey)

    def fill(self, item_type):
        self.__rename.setVisible(False)
        self.__replace_step.setVisible(False)
        self.__set_hotkey.setVisible(False)

        if item_type == UI.STEP or \
                item_type == UI.ACTION or \
                item_type == UI.ACTION_GROUP:
            self.__rename.setVisible(True)

        if item_type == UI.STEP:
            self.__replace_step.setVisible(True)

        if item_type == UI.ACTION:
            self.__set_hotkey.setVisible(True)

    def on_rename_menu(self):
        Facade.getInstance().sendNotification(Notes.CONTEXT_MENU_RENAME)

    def on_replace_step(self):
        Facade.getInstance().sendNotification(Notes.CONTEXT_MENU_REPLACE_STEP)

    def on_set_hotkey(self):
        Facade.getInstance().sendNotification(Notes.CONTEXT_MENU_SET_HOTKEY)
