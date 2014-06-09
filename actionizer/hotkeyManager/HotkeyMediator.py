from hotkeyManager.hotkeylist import HotkeyList
from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator
from hotkeyManager import Hotkey

__author__ = 'c0ffee'


class HotkeyMediator(Mediator):
    NAME = "HotkeyMediator"

    def __init__(self):
        """:type :Hotkey"""
        super(HotkeyMediator, self).__init__(HotkeyMediator.NAME, None)
        self.__hotkey_list = HotkeyList()
        self.__hotkey = Hotkey(self.__hotkey_list.hotkey_actions)
        self.setViewComponent(self.__hotkey)

    def listNotificationInterests(self):
        return [
            Notes.START_LISTEN_GLOBAL_HOTKEYS,
            Notes.STOP_LISTEN_GLOBAL_HOTKEYS,
            Notes.PAUSE_LISTEN_GLOBAL_HOTKEYS,
            Notes.UNPAUSE_LISTEN_GLOBAL_HOTKEYS,
            Notes.HOTKEY_CHANGED,
            Notes.TREE_MODEL_LOADED,
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

        elif note.name == Notes.HOTKEY_CHANGED:
            vo = note.body
            """:type :HotkeyChangedVO"""
            self.__hotkey_list.add_hotkey(vo.node.leaf.hotkey, vo.node)

        elif note.name == Notes.TREE_MODEL_LOADED:
            root_node = note.body["root"]
            self.__hotkey_list.update(root_node)

    def __is_listening(self):
        return self.__hotkey.is_listening
