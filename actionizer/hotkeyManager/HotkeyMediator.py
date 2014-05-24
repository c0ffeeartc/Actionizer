from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator
from hotkeyManager import Hotkey
from mainWindow.MainWindowMediator import MainWindowMediator

__author__ = 'c0ffee'


class HotkeyMediator(Mediator):
    def onRegister(self):
        super(HotkeyMediator, self).onRegister()
        main_window = self.facade.retrieveMediator(MainWindowMediator.NAME).getViewComponent()
        self.setViewComponent(Hotkey(main_window))

    def listNotificationInterests(self):
        return [
            Notes.START_LISTEN_GLOBAL_HOTKEYS,
            Notes.STOP_LISTEN_GLOBAL_HOTKEYS,
        ]

    def handleNotification(self, note):
        if note.name == Notes.START_LISTEN_GLOBAL_HOTKEYS:
            self.getHotkeyManager().is_listening = True
        elif note.name == Notes.STOP_LISTEN_GLOBAL_HOTKEYS:
            self.getHotkeyManager().is_listening = False
            pass

    def getHotkeyManager(self):
        return self.viewComponent
