from actionTree.TreeModelProxy import TreeModelProxy
from contextMenu.contextMenuMediator import ContextMenuMediator
from mainWindow.NewTreeElementCommand import NewTreeElementCommand
from notifications.notes import Notes
from stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.command import SimpleCommand
from hotkeyManager.HotkeyMediator import HotkeyMediator
from mainWindow.MainWindowMediator import MainWindowMediator
from textDialog.textDialogMediator import TextDialogMediator
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
        self.facade.registerMediator(TextDialogMediator())
        self.facade.registerMediator(MainWindowMediator())
        self.facade.registerMediator(ContextMenuMediator())
        self.facade.registerMediator(HotkeyMediator())
        # ...

        # post children
        self.sendNotification(Notes.TREE_MODEL_LOAD)
