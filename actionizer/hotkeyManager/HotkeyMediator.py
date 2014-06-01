from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator
from hotkeyManager import Hotkey
from mainWindow.MainWindowMediator import MainWindowMediator

__author__ = 'c0ffee'


class HotkeyMediator(Mediator):
    NAME = "HotkeyMediator"

    def __init__(self):
        """:type :Hotkey"""
        super(HotkeyMediator, self).__init__(HotkeyMediator.NAME, None)
        main_window = self.facade.retrieveMediator(MainWindowMediator.NAME).getViewComponent()
        self.__hotkey = Hotkey(main_window)
        self.setViewComponent(self.__hotkey)

    def listNotificationInterests(self):
        return [
            Notes.START_LISTEN_GLOBAL_HOTKEYS,
            Notes.STOP_LISTEN_GLOBAL_HOTKEYS,
            Notes.PAUSE_LISTEN_GLOBAL_HOTKEYS,
            Notes.UNPAUSE_LISTEN_GLOBAL_HOTKEYS,
        ]

    def handleNotification(self, note):
        if note.name == Notes.START_LISTEN_GLOBAL_HOTKEYS:
            self.__hotkey.is_listening = True
        elif note.name == Notes.STOP_LISTEN_GLOBAL_HOTKEYS:
            self.__hotkey.is_listening = False
        elif note.name == Notes.PAUSE_LISTEN_GLOBAL_HOTKEYS:
            self.__hotkey.is_listening_paused = True
        elif note.name == Notes.UNPAUSE_LISTEN_GLOBAL_HOTKEYS:
            self.__hotkey.is_listening_paused = False

    def __is_listening(self):
        return self.__hotkey.is_listening
