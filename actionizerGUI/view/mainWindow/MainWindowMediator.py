import Notes
from puremvc.patterns.mediator import Mediator
from view.mainWindow.MainWindow import MainWindow

__author__ = 'cfe'


class MainWindowMediator(Mediator):
    NAME = "MainWindowMediator"

    def onRegister(self):
        super(MainWindowMediator, self).onRegister()
        self.setViewComponent(MainWindow())

    def listNotificationInterests(self):
        return[
            Notes.STEP_CONTEXT_MENU_SELECTED,
        ]

    def handleNotification(self, note):
        if note.name == Notes.STEP_CONTEXT_MENU_SELECTED:
            # replaces step
            step_uid = note.body["step_uid"]
            tree = self.get_main_window().tree
            old_item = tree.currentItem()
            item_parent = old_item.parent()
            old_item_index = old_item.parent().indexOfChild(old_item)
            item_parent.removeChild(old_item)
            self.get_main_window().add_step(step_uid, item_parent, old_item_index)

    def get_main_window(self):
        return self.viewComponent
