from PySide.QtCore import QModelIndex
from notifications.notes import Notes, TreeModelExpandedVO
from puremvc.patterns.mediator import Mediator
from treemdl.model.treenode import TreeNode
from treemdl.treemodel2proxy import TreeModel2Proxy
from treeview2.view.treeview import TreeView

__author__ = 'c0ffee'


class TreeView2Mediator(Mediator):
    NAME = "TreeView2Mediator"  # uses TreeViewMediator to replace old mediator

    def __init__(self):
        super(TreeView2Mediator, self).__init__(TreeView2Mediator.NAME)
        self.__model_proxy = self.facade.retrieveProxy(TreeModel2Proxy.NAME)
        """:type :TreeModel2Proxy"""
        self.__tree_view = TreeView()
        self.__tree_view.setModel(self.__model_proxy.get_model())
        # noinspection PyUnresolvedReferences
        self.__tree_view.expanded.connect(self.on_expanded)
        self.setViewComponent(self.__tree_view)

    def listNotificationInterests(self):
        return [
            Notes.TREE_MODEL_SAVE,
            Notes.TREE_MODEL_LOAD,
            Notes.TREE_MODEL_LOADED,
            Notes.TREE_MODEL_EXPANDED,
            Notes.TREE_MODEL_REMOVE,
            Notes.TREE_MODEL_REMOVED,
        ]

    def handleNotification(self, note):
        """:type :TreeModel2Proxy"""
        if note.name == Notes.TREE_MODEL_LOAD:
            self.__model_proxy.load()

        if note.name == Notes.TREE_MODEL_LOADED:
            # TODO: expand nodes from loaded is_expanded data
            pass
            # self.__tree_view.reset()

        if note.name == Notes.TREE_MODEL_SAVE:
            self.__model_proxy.save()

        if note.name == Notes.TREE_MODEL_EXPANDED:
            vo = note.body
            """:type :TreeModelExpandedVO"""
            self.__model_proxy.set_is_expanded(vo.has_expanded, vo.index)

        elif note.name == Notes.TREE_MODEL_REMOVE:
            self.__model_proxy.remove(self.get_current_q_index())

        elif note.name == Notes.TREE_MODEL_REMOVED:
            """:type :list"""

    def on_expanded(self, index):
        """
        :type index: QModelIndex
        """
        self.facade.sendNotification(Notes.TREE_MODEL_EXPANDED, TreeModelExpandedVO(True, index))

    def on_collapsed(self, index):
        """
        :type index: QModelIndex
        """
        self.facade.sendNotification(Notes.TREE_MODEL_EXPANDED, TreeModelExpandedVO(False, index))

    def get_current_node(self):
        """:rtype :TreeNode"""
        cur_index = self.__tree_view.currentIndex()
        """:type :QModelIndex"""
        return cur_index.internalPointer()

    def get_current_q_index(self):
        return self.__tree_view.currentIndex()
