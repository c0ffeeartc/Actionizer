from actionTree.TreeModelProxy import TreeModelProxy
from mainWindow.NewTreeElementCommand import NewTreeElementCommand
from stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.command import SimpleCommand
from hotkeyManager.HotkeyMediator import HotkeyMediator
from mainWindow.MainWindowMediator import MainWindowMediator
from treeView.TreeViewMediator import TreeViewMediator

__author__ = 'cfe'


class StartupCommand(SimpleCommand):
    def execute(self, notification):
        print("hello, StartupCommand")

        # registerCommands
        self.facade.registerCommand(NewTreeElementCommand.NAME, NewTreeElementCommand)
        # ...

        # registerProxies
        self.facade.registerProxy(StepPoolProxy())
        tree_model_proxy = TreeModelProxy()
        self.facade.registerProxy(tree_model_proxy)
        # ...

        # registerMediator
        self.facade.registerMediator(TreeViewMediator())
        self.facade.registerMediator(MainWindowMediator())
        self.facade.registerMediator(HotkeyMediator())
        # ...

        # post children
        tree_model_proxy.load()