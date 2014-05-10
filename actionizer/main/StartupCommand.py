from stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.command import SimpleCommand
from hotkeyManager.HotkeyMediator import HotkeyMediator
from mainWindow.MainWindowMediator import MainWindowMediator

__author__ = 'cfe'


class StartupCommand(SimpleCommand):
    def execute(self, notification):
        print("hello, StartupCommand")

        # registerCommands
        # ...

        # registerProxies
        self.facade.registerProxy(StepPoolProxy())
        # ...

        # registerMediator
        self.facade.registerMediator(MainWindowMediator())
        self.facade.registerMediator(HotkeyMediator())
        # ...

        # post actions
