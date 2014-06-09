from combodialog.combodialogmediator import ComboDialogMediator
from commands.replacestepcommand import ReplaceStepCommand
from contextMenu.contextMenuMediator import ContextMenuMediator
from hotkeydialog.hotkeydialogmediator import HotkeyDialogMediator
from mainWindow.NewTreeElementCommand import NewTreeElementCommand
from notifications.notes import Notes
from stepPool.StepPoolProxy import StepPoolProxy
from puremvc.patterns.command import SimpleCommand
from hotkeyManager.HotkeyMediator import HotkeyMediator
from mainWindow.MainWindowMediator import MainWindowMediator
from textDialog.textDialogMediator import TextDialogMediator
from treemdl.treemodel2proxy import TreeModel2Proxy
from treeview2.treeview2mediator import TreeView2Mediator

__author__ = 'cfe'


class StartupCommand(SimpleCommand):
    def execute(self, notification):
        print("hello, StartupCommand")

        # registerCommands
        self.facade.registerCommand(NewTreeElementCommand.NAME, NewTreeElementCommand)
        self.facade.registerCommand(Notes.REPLACE_STEP_COMMAND, ReplaceStepCommand)
        # ...

        # registerProxies
        self.facade.registerProxy(StepPoolProxy())
        tree_model_proxy = TreeModel2Proxy()
        self.facade.registerProxy(tree_model_proxy)
        # ...

        # registerMediator
        self.facade.registerMediator(TreeView2Mediator())
        self.facade.registerMediator(TextDialogMediator())
        self.facade.registerMediator(ComboDialogMediator())
        self.facade.registerMediator(HotkeyDialogMediator())
        self.facade.registerMediator(MainWindowMediator())
        self.facade.registerMediator(ContextMenuMediator())
        self.facade.registerMediator(HotkeyMediator())
        # ...

        # post children
        self.sendNotification(Notes.TREE_MODEL_LOAD)
