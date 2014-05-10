from PySide.QtGui import QMenu

from stepPool.StepPoolProxy import StepPoolProxy
from notifications import Notes
from puremvc.patterns.facade import Facade


__author__ = 'c0ffee'


class StepContextMenu(QMenu):
    menu_steps = None

    def __init__(self, *args, **kwargs):
        super(StepContextMenu, self).__init__(*args, **kwargs)
        self.menu_steps = Facade.getInstance().retrieveProxy(StepPoolProxy.NAME).get_step_files()
        self.fill()
        self.triggered.connect(self.handle_click)

    def fill(self):
        self.clear()
        for step in self.menu_steps:
            self.addAction(step)

    def handle_click(self, action):
        Facade.getInstance().sendNotification(
            Notes.STEP_CONTEXT_MENU_SELECTED,
            {
                "step_uid": action.text(),
                "point": (self.pos())
            },
        )
