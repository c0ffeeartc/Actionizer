import pyHook

__author__ = 'c0ffee'


class Hotkey(object):
    hm = None
    def __init__(self):
        self.hm = pyHook.HookManager()
        self.hm.HookKeyboard()
        self.hm.KeyUp = self.on_key_up

    def on_key_up(self, event):
        isCtrl = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_CONTROL")))
        isAlt = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_MENU")))
        # isAlt = bool(pyHook.GetKeyState(pyHook.HookConstants.VKeyToID("VK_ALT")))
        if isCtrl and isAlt and event.Key == "P":
            print("Pressed Ctrl+Alt+P")
        # print(isCtrl)
        # print(isAlt)
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
        return True
