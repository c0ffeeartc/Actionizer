from PySide.QtCore import QTimer
from PySide.QtGui import QKeySequence
import pyHook

__author__ = 'c0ffee'


class Hotkey(object):
    def __init__(self, hotkey_list):
        self.hotkey_manager = pyHook.HookManager()
        self.hotkey_manager.HookKeyboard()
        self.hotkey_manager.KeyUp = self.on_key
        self.hotkey_manager.KeyDown = self.on_key
        self.is_listening = False
        self.pressed = {}
        self.key_que = []
        self.hotkey_actions = hotkey_list

        self.is_listening_paused = False

        self.timer = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.process_key_events)
        self.timer.start(50)

    def process_key_events(self):
        while self.key_que:
            key_seq = self.key_que.pop(0)
            self.hotkey_actions[key_seq].play()

    def on_key(self, event):
        """
        @type event: KeyboardEvent
        @return:
        """
        if self.is_listening and not self.is_listening_paused:
            # print(event.Key)

            is_ctrl = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_CONTROL")))
            is_alt = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_MENU")))
            is_shift = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_SHIFT")))

            key_seq = ""
            if is_ctrl:
                key_seq += "Ctrl+"
            if is_alt:
                key_seq += "Alt+"
            if is_shift:
                key_seq += "Shift+"
            key_seq += QKeySequence(event.Key).toString()

            if key_seq in self.hotkey_actions.keys():
                if event.Message == pyHook.HookConstants.WM_KEYDOWN or\
                        event.Message == pyHook.HookConstants.WM_SYSKEYDOWN:
                    if key_seq not in self.pressed.keys():
                        print("Hotkey: " + key_seq)
                        self.key_que.append(key_seq)
                        self.pressed[key_seq] = True
                    return False
                del self.pressed[key_seq]
                # self.key_que.append(key_seq)
                return False
        return True
        # print 'MessageName:', event.MessageName
        # print 'Message:', event.Message
        # print 'Time:', event.Time
        # noinspection PyUnreachableCode
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
