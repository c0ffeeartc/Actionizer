from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator
from treemdl.treemodel2proxy import TreeModel2Proxy
from treeview2.view.treeview import TreeView

__author__ = 'c0ffee'


class TreeView2Mediator(Mediator):
    NAME = "TreeViewMediator"  # uses TreeViewMediator to replace old mediator

    def __init__(self):
        super(TreeView2Mediator, self).__init__(TreeView2Mediator.NAME)
        self.model_proxy = self.facade.retrieveProxy(TreeModel2Proxy.NAME)
        """:type :TreeModel2Proxy"""
        self.__tree_view = TreeView()
        self.__tree_view.setModel(self.model_proxy.get_model())
        self.setViewComponent(self.__tree_view)

    def listNotificationInterests(self):
        return [
            Notes.TREE_MODEL_LOAD,
            Notes.TREE_MODEL_LOADED,
        ]

    def handleNotification(self, note):
        if note.name == Notes.TREE_MODEL_LOAD:
            self.model_proxy.load()

    def get_cur_item(self):
        cur_index = self.__tree_view.currentIndex()
        """:type :QModelIndex"""
        return cur_index.internalPointer()