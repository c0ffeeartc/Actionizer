from PySide.QtCore import QTimer
from PySide.QtGui import QKeySequence
# import pyHook
from pyHook.HookManager import *
from activeappinfo.activeappinfo import ActiveAppInfo
import win32com.client
from hotkeyManager.remaplist import RemapList

__author__ = 'c0ffee'


class Hotkey(object):
    def __init__(self, hotkey_list):
        self.hotkey_manager = HookManager()
        self.hotkey_manager.HookKeyboard()
        self.hotkey_manager.KeyUp = self.on_key
        self.hotkey_manager.KeyDown = self.on_key
        self.is_listening = False
        self.pressed = {}
        self.key_que = []
        self.app_info = ActiveAppInfo()
        self.remap = RemapList()
        self.is_waiting_modifier_up = False
        self.hotkey_list = hotkey_list
        """:type :dict"""
        self.shell = win32com.client.Dispatch("WScript.Shell")

        self.is_listening_paused = False
        self.is_photoshop = False

        self.timer = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.process_key_events)
        self.timer.start(30)

    def process_key_events(self):
        while self.key_que:
            key_seq = self.key_que.pop(0)
            # fixme: first keystroke outside photoshop is blocked by is_photoshop
            # is_photoshop should update itself on changing window
            self.is_photoshop = self.app_info.is_photoshop()
            if key_seq in self.remap.remap_list.keys() and self.is_photoshop:
                print("Remap: " + key_seq + " to " + self.remap.remap_list[key_seq])
                self.shell.sendKeys(self.remap.remap_list[key_seq])
            elif key_seq in self.hotkey_list.keys() and self.is_photoshop:
                print("Hotkey: " + key_seq)
                self.hotkey_list[key_seq].play()

    def on_key(self, event):
        """
        @type event: pyHook.HookManager.KeyboardEvent
        @return:
        """
        if self.is_listening and not self.is_listening_paused:
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

            is_ctrl = bool(GetKeyState(HookConstants.VKeyToID("VK_CONTROL")))
            is_alt = bool(GetKeyState(HookConstants.VKeyToID("VK_MENU")))
            is_shift = bool(GetKeyState(HookConstants.VKeyToID("VK_SHIFT")))

            key_seq = ""
            if is_ctrl:
                key_seq += "Ctrl+"
            if is_alt:
                key_seq += "Alt+"
            if is_shift:
                key_seq += "Shift+"
            key_seq += QKeySequence(event.Key).toString()
            if key_seq in self.remap.remap_list.keys():
                return self.add_key_seq_to_que(key_seq, event)

            elif not event.IsInjected() and key_seq in self.hotkey_list.keys():
                return self.add_key_seq_to_que(key_seq, event)
        return True

    def add_key_seq_to_que(self, key_seq, event):
        if event.Message == HookConstants.WM_KEYDOWN or \
                event.Message == HookConstants.WM_SYSKEYDOWN:
            if key_seq not in self.pressed.keys():
                # if is_ctrl or is_alt or is_shift:
                #     self.is_waiting_modifier_up = True
                self.key_que.append(key_seq)
                self.pressed[key_seq] = True
            if self.is_photoshop:
                return False
            else:
                return True

        if key_seq in self.pressed.keys():
            del self.pressed[key_seq]
        else:
            print ("no such key in pressed")

        if self.is_photoshop:
            return False
        else:
            return True

    # todo: test with various key sequences
    def send_key_seq(self, key_seq):
        """
        :type key_seq: str
        """
        buttons = key_seq.split("+")
        key_seq_formatted = ""
        if "Ctrl" in buttons:
            key_seq_formatted += RemapList.CTRL
        if "Alt" in buttons:
            key_seq_formatted += RemapList.ALT
        if "Shift" in buttons:
            key_seq_formatted += RemapList.SHIFT
        key_seq_formatted += buttons[-1].upper()
        self.shell.sendKeys(key_seq_formatted)
