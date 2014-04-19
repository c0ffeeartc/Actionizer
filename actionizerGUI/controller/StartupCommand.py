from puremvc.patterns.command import SimpleCommand
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
        # ...

        # post actions
