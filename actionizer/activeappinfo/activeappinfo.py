import win32gui
import win32process
import wmi

__author__ = 'cfe'


class ActiveAppInfo(object):
    def __init__(self):
        self.wmi = wmi.WMI()

    def get_active_app_name(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            for p in self.wmi.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
                exe = p.Name
                break
        except :
            return None
        else:
            # noinspection PyUnboundLocalVariable
            return exe

    def is_photoshop(self):
        return "Photoshop.exe" == self.get_active_app_name()