from PySide.QtCore import QTimer
import pyHook

__author__ = 'c0ffee'


class Hotkey(object):
    hotkey_manager = None
    key_que = []
    timer = None
    main_window = None
    is_listening = False
    is_listening_paused = False

    def __init__(self, main_window):
        self.hotkey_manager = pyHook.HookManager()
        self.hotkey_manager.HookKeyboard()
        self.hotkey_manager.KeyUp = self.on_key
        self.hotkey_manager.KeyDown = self.on_key
        self.is_listening = False

        self.main_window = main_window

        self.timer = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.process_key_events)
        self.timer.start(1000)

    def process_key_events(self):
        while self.key_que:
            self.main_window.handle_key(self.key_que.pop(0))

    def on_key(self, event):
        if self.is_listening and not self.is_listening_paused:
            self.key_que.append(event)
        return True

        # is_ctrl = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_CONTROL")))
        # is_alt = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_MENU")))
        # print 'MessageName:', event.MessageName
        # print 'Message:', event.Message
        # print 'Time:', event.Time
        # print 'Window:', event.Window
        # print 'WindowName:', event.WindowName
        # print 'Ascii:', event.Ascii, chr(event.Ascii)
        # print 'Key:', event.Key
        # print 'KeyID:', event.KeyID
        # print 'ScanCode:', event.ScanCode
        # print 'Extended:', event.Extended
        # print 'Injected:', event.Injected
        # print 'Alt', event.Alt
        # print 'Transition', event.Transition
        # print '---'
