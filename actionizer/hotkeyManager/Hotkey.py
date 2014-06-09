from PySide.QtCore import QTimer
from PySide.QtGui import QKeySequence
import pyHook
from notifications.notes import Notes
from puremvc.patterns.facade import Facade

__author__ = 'c0ffee'


class Hotkey(object):
    def __init__(self, hotkey_list):
        self.hotkey_manager = pyHook.HookManager()
        self.hotkey_manager.HookKeyboard()
        # self.hotkey_manager.KeyUp = self.on_key
        self.hotkey_manager.KeyDown = self.on_key
        self.is_listening = False
        self.key_que = []
        self.hotkey_actions = hotkey_list

        self.is_listening_paused = False

        self.timer = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.process_key_events)
        self.timer.start(100)

    def process_key_events(self):
        while self.key_que:
            key_event = self.key_que.pop(0)
            self.handle_key(key_event)

    def on_key(self, event):
        if self.is_listening and not self.is_listening_paused:
            print(event.Key)
            self.key_que.append(event)
        # return True

        is_ctrl = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_CONTROL")))
        is_alt = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_MENU")))

        key_seq = ""
        if is_ctrl:
            key_seq += "Ctrl+"
        if is_alt:
            key_seq += "Alt+"
        key_seq += QKeySequence(event.Key).toString()
        for hotkey in self.hotkey_actions.keys():
            if key_seq == hotkey:
                print("Found hotkey")
                return True

        # is_ctrl = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_CONTROL")))
        # is_alt = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_MENU")))
        # print 'MessageName:', event.MessageName
        # print 'Message:', event.Message
        # print 'Time:', event.Time
        print 'Window:', event.Window
        print 'WindowName:', event.WindowName
        # print 'Ascii:', event.Ascii, chr(event.Ascii)
        # print 'Key:', event.Key
        # print 'KeyID:', event.KeyID
        # print 'ScanCode:', event.ScanCode
        # print 'Extended:', event.Extended
        # print 'Injected:', event.Injected
        # print 'Alt', event.Alt
        # print 'Transition', event.Transition
        # print '---'
        return True

    def handle_key(self, key_event):
        is_ctrl = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_CONTROL")))
        is_alt = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_MENU")))

        key_seq = ""
        if is_ctrl:
            key_seq += "Ctrl+"
        if is_alt:
            key_seq += "Alt+"
        key_seq += QKeySequence(key_event.Key).toString()

        for hotkey in self.hotkey_actions.keys():
            if key_seq == hotkey:
                self.hotkey_actions[key_seq].play()

        if key_event.Key == "P":
            Facade.getInstance().sendNotification(Notes.START_LISTEN_GLOBAL_HOTKEYS)
        elif key_event.Key == "Q":
            Facade.getInstance().sendNotification(Notes.STOP_LISTEN_GLOBAL_HOTKEYS)
        elif key_event.Key == "A":
            pass
        print(key_event.Key + " " + key_event.MessageName)
