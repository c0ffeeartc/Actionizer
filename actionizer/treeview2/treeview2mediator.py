from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator
from treemdl.treemodel2proxy import TreeModel2Proxy
from treeview2.view.treeview import TreeView

__author__ = 'c0ffee'


class TreeView2Mediator(Mediator):
    NAME = "TreeView2Mediator"

    def __init__(self):
        super(TreeView2Mediator, self).__init__(TreeView2Mediator.NAME)
        model_proxy = self.facade.retrieveProxy(TreeModel2Proxy.NAME)
        """:type :TreeModel2Proxy"""
        self.__tree_view = TreeView()
        self.__tree_view.setModel(model_proxy.data)
        self.setViewComponent(self.__tree_view)

    def listNotificationInterests(self):
        return [
            Notes.TREE_MODEL_LOADED,
        ]

    def handleNotification(self, note):
        pass
