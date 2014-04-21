from puremvc.patterns.command import SimpleCommand
from view.hotkeyManager.HotkeyMediator import HotkeyMediator
from view.mainWindow.MainWindowMediator import MainWindowMediator

__author__ = 'cfe'


class StartupCommand(SimpleCommand):
    def execute(self, notification):
        print("hello, StartupCommand")

        # registerCommands
        # ...

        # registerProxies
        # ...

        # registerMediator
        self.facade.registerMediator(MainWindowMediator())
        self.facade.registerMediator(HotkeyMediator())
        # ...

        # post actions
