from PySide.QtGui import QMenu

from stepPool.StepPoolProxy import StepPoolProxy
from notifications.notes import Notes
from puremvc.patterns.facade import Facade


__author__ = 'c0ffee'


class ContextMenuView(QMenu):
    menu_steps = None

    def __init__(self, *args, **kwargs):
        super(ContextMenuView, self).__init__(*args, **kwargs)
        self.menu_steps = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME).get_step_files()
        self.fill()
        # noinspection PyUnresolvedReferences
        self.triggered.connect(self.handle_click)

    def fill(self):
        self.clear()
        self.addAction("&Rename")
        self.addSeparator()
        for step in self.menu_steps:
            self.addAction(step)

    def handle_click(self, action):
        Facade.getInstance().sendNotification(
            Notes.CONTEXT_MENU_SELECTED,
            {
                "txt": action.text(),
                "point": (self.pos())
            },
        )
