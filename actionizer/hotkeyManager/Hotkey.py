from PySide.QtCore import QTimer
from PySide.QtGui import QKeySequence
from pyHook.HookManager import *
import win32api
import win32con
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

        self.is_holding_left_ctrl = False
        self.is_holding_left_alt = False
        self.is_holding_left_shift = False

        self.is_holding_right_ctrl = False
        self.is_holding_right_alt = False
        self.is_holding_right_shift = False

        self.is_left_ctrl_down_injected = False
        self.is_left_ctrl_up_injected = False
        self.is_left_alt_down_injected = False
        self.is_left_alt_up_injected = False
        self.is_left_shift_down_injected = False
        self.is_left_shift_up_injected = False

        self.is_right_ctrl_down_injected = False
        self.is_right_ctrl_up_injected = False
        self.is_right_alt_down_injected = False
        self.is_right_alt_up_injected = False
        self.is_right_shift_down_injected = False
        self.is_right_shift_up_injected = False

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

    # fixme: slows down response from keyboard
    # fixme: sometimes program leaves injected keydowns on exit, and breaks keyboard input
    def on_key(self, event):
        """
        @type event: pyHook.HookManager.KeyboardEvent
        @return:
        """
        if self.is_listening and not self.is_listening_paused:
            if event.IsInjected():
                print '--- Injected Key:', event.Key, '- MessageName:', event.MessageName
                self.set_injected_flags(event)
                return True
            # self.print_event(event)

            self.update_hold_flags(event)
            self.fix_modifiers()

            key_seq = ""
            if self.is_holding_left_ctrl or self.is_holding_right_ctrl:
                key_seq += "Ctrl+"
            if self.is_holding_left_alt or self.is_holding_right_alt:
                key_seq += "Alt+"
            if self.is_holding_left_shift or self.is_holding_right_shift:
                key_seq += "Shift+"

            key_seq += QKeySequence(event.Key).toString()
            if key_seq in self.remap.remap_list.keys():
                return self.add_key_seq_to_que(key_seq, event)

            elif key_seq in self.hotkey_list.keys():
                return self.add_key_seq_to_que(key_seq, event)
        return True

    def print_event(self, event):
        print 'MessageName:', event.MessageName
        print 'Message:', event.Message
        print 'Time:', event.Time
        print 'Window:', event.Window
        print 'WindowName:', event.WindowName
        print 'Ascii:', event.Ascii, chr(event.Ascii)
        print 'Key:', event.Key
        print 'KeyID:', event.KeyID
        print 'ScanCode:', event.ScanCode
        print 'Extended:', event.Extended
        print 'Injected:', event.Injected
        print 'Alt', event.Alt
        print 'Transition', event.Transition
        print '---'

    def update_hold_flags(self, event):
        if event.Message == HookConstants.WM_KEYDOWN or event.Message == HookConstants.WM_SYSKEYDOWN:
            if event.KeyID == win32con.VK_LMENU:
                self.is_holding_left_alt = True

            elif event.KeyID == win32con.VK_LCONTROL:
                self.is_holding_left_ctrl = True
                
            elif event.KeyID == win32con.VK_LSHIFT:
                self.is_holding_left_shift = True

            elif event.KeyID == win32con.VK_RMENU:
                self.is_holding_right_alt = True

            elif event.KeyID == win32con.VK_RCONTROL:
                self.is_holding_right_ctrl = True

            elif event.KeyID == win32con.VK_RSHIFT:
                self.is_holding_right_shift = True

        elif event.Message == HookConstants.WM_KEYUP or event.Message == HookConstants.WM_SYSKEYUP:
            if event.KeyID == win32con.VK_LMENU:
                self.is_holding_left_alt = False

            elif event.KeyID == win32con.VK_LCONTROL:
                self.is_holding_left_ctrl = False

            elif event.KeyID == win32con.VK_LSHIFT:
                self.is_holding_left_shift = False

            elif event.KeyID == win32con.VK_RMENU:
                self.is_holding_right_alt = False

            elif event.KeyID == win32con.VK_RCONTROL:
                self.is_holding_right_ctrl = False

            elif event.KeyID == win32con.VK_RSHIFT:
                self.is_holding_right_shift = False

    def set_injected_flags(self, event):
        if event.Message == HookConstants.WM_KEYUP or event.Message == HookConstants.WM_SYSKEYUP:
            if event.KeyID == win32con.VK_LMENU:
                self.is_left_alt_up_injected = True
            elif event.KeyID == win32con.VK_LCONTROL:
                self.is_left_ctrl_up_injected = True
            elif event.KeyID == win32con.VK_LSHIFT:
                self.is_left_shift_up_injected = True
            elif event.KeyID == win32con.VK_RMENU:
                self.is_right_alt_up_injected = True
            elif event.KeyID == win32con.VK_RCONTROL:
                self.is_right_ctrl_up_injected = True
            elif event.KeyID == win32con.VK_RSHIFT:
                self.is_right_shift_up_injected = True

        elif event.Message == HookConstants.WM_KEYDOWN or event.Message == HookConstants.WM_SYSKEYDOWN:
            if event.KeyID == win32con.VK_LMENU:
                self.is_left_alt_down_injected = True
            elif event.KeyID == win32con.VK_LCONTROL:
                self.is_left_ctrl_down_injected = True
            elif event.KeyID == win32con.VK_LSHIFT:
                self.is_left_shift_down_injected = True
            elif event.KeyID == win32con.VK_RMENU:
                self.is_right_alt_down_injected = True
            elif event.KeyID == win32con.VK_RCONTROL:
                self.is_right_ctrl_down_injected = True
            elif event.KeyID == win32con.VK_RSHIFT:
                self.is_right_shift_down_injected = True

    def fix_modifiers(self):
        self.fix_vk(win32con.VK_LMENU, self.is_holding_left_alt, self.set_is_left_alt_down_injected, self.set_is_left_alt_up_injected)
        self.fix_vk(win32con.VK_LCONTROL, self.is_holding_left_ctrl, self.set_is_left_ctrl_down_injected, self.set_is_left_ctrl_up_injected)
        self.fix_vk(win32con.VK_LSHIFT, self.is_holding_left_shift, self.set_is_left_shift_down_injected, self.set_is_left_shift_up_injected)

        self.fix_vk(win32con.VK_RMENU, self.is_holding_right_alt, self.set_is_right_alt_down_injected, self.set_is_right_alt_up_injected)
        self.fix_vk(win32con.VK_RCONTROL, self.is_holding_right_ctrl, self.set_is_right_ctrl_down_injected, self.set_is_right_ctrl_up_injected)
        self.fix_vk(win32con.VK_RSHIFT, self.is_holding_right_shift, self.set_is_right_shift_down_injected, self.set_is_right_shift_up_injected)

    def fix_vk(self, vk_id, flag_holding, setter_injected_down, setter_injected_up):
        if flag_holding and setter_injected_up():
            # print "injecting " + HookConstants.id_to_vk[vk_id]
            win32api.keybd_event(vk_id, 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
            setter_injected_down(True)
            setter_injected_up(False)

        elif setter_injected_down() and not flag_holding:
            # print "fixing " + HookConstants.id_to_vk[vk_id]
            win32api.keybd_event(vk_id, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
            setter_injected_down(False)

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

    # -----------------------------------------
    # Setters
    # -----------------------------------------
    def set_is_left_alt_down_injected(self, value=None):
        if value is None:
            return self.is_left_alt_down_injected
        self.is_left_alt_down_injected = value

    def set_is_right_alt_down_injected(self, value=None):
        if value is None:
            return self.is_right_alt_down_injected
        self.is_right_alt_down_injected = value

    def set_is_left_ctrl_down_injected(self, value=None):
        if value is None:
            return self.is_left_ctrl_down_injected
        self.is_left_ctrl_down_injected = value

    def set_is_right_ctrl_down_injected(self, value=None):
        if value is None:
            return self.is_right_ctrl_down_injected
        self.is_right_ctrl_down_injected = value

    def set_is_left_shift_down_injected(self, value=None):
        if value is None:
            return self.is_left_shift_down_injected
        self.is_left_shift_down_injected = value

    def set_is_right_shift_down_injected(self, value=None):
        if value is None:
            return self.is_right_shift_down_injected
        self.is_right_shift_down_injected = value

    def set_is_left_alt_up_injected(self, value=None):
        if value is None:
            return self.is_left_alt_up_injected
        self.is_left_alt_up_injected = value

    def set_is_right_alt_up_injected(self, value=None):
        if value is None:
            return self.is_right_alt_up_injected
        self.is_right_alt_up_injected = value

    def set_is_left_ctrl_up_injected(self, value=None):
        if value is None:
            return self.is_left_ctrl_up_injected
        self.is_left_ctrl_up_injected = value

    def set_is_right_ctrl_up_injected(self, value=None):
        if value is None:
            return self.is_right_ctrl_up_injected
        self.is_right_ctrl_up_injected = value

    def set_is_left_shift_up_injected(self, value=None):
        if value is None:
            return self.is_left_shift_up_injected
        self.is_left_shift_up_injected = value

    def set_is_right_shift_up_injected(self, value=None):
        if value is None:
            return self.is_right_shift_up_injected
        self.is_right_shift_up_injected = value
    # -------------------------------------