from PySide.QtCore import QModelIndex
from notifications.notes import Notes, TreeModelExpandedVO, ShowContextMenuVO
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
        self.__tree_view = TreeView(self.__model_proxy.get_model())
        # noinspection PyUnresolvedReferences
        self.__tree_view.expanded.connect(self.on_expanded)
        # noinspection PyUnresolvedReferences
        self.__tree_view.collapsed.connect(self.on_collapsed)
        self.setViewComponent(self.__tree_view)
        # noinspection PyUnresolvedReferences
        self.__tree_view.customContextMenuRequested.connect(self.show_menu)

    def listNotificationInterests(self):
        return [
            Notes.TREE_MODEL_SAVE,
            Notes.TREE_MODEL_SAVED,
            Notes.TREE_MODEL_LOAD,
            Notes.TREE_MODEL_LOADED,
            Notes.TREE_ITEM_PLAY,
            Notes.TREE_MODEL_EXPANDED,
            Notes.TREE_MODEL_REMOVE,
            Notes.TREE_MODEL_REMOVED,
        ]

    def handleNotification(self, note):
        """:type :TreeModel2Proxy"""
        if note.name == Notes.TREE_MODEL_LOAD:
            self.__model_proxy.load()

        elif note.name == Notes.TREE_MODEL_LOADED:
            # TODO: expand nodes from loaded is_expanded data
            pass
            # self.__tree_view.reset()

        elif note.name == Notes.TREE_MODEL_SAVE:
            self.__model_proxy.save()

        elif note.name == Notes.TREE_MODEL_SAVED:
            print("saved")

        elif note.name == Notes.TREE_MODEL_EXPANDED:
            vo = note.body
            """:type :TreeModelExpandedVO"""
            self.__model_proxy.set_is_expanded(vo.has_expanded, vo.index)

        elif note.name == Notes.TREE_ITEM_PLAY:
            cur = self.get_current_node()
            self.get_current_node().play()

        elif note.name == Notes.TREE_MODEL_REMOVE:
            self.__model_proxy.remove(self.get_current_q_index())

        elif note.name == Notes.TREE_MODEL_REMOVED:
            pass

    def on_expanded(self, q_index):
        """
        :type q_index: QModelIndex
        """
        self.facade.sendNotification(Notes.TREE_MODEL_EXPANDED, TreeModelExpandedVO(True, q_index))

    def on_collapsed(self, q_index):
        """
        :type q_index: QModelIndex
        """
        self.facade.sendNotification(Notes.TREE_MODEL_EXPANDED, TreeModelExpandedVO(False, q_index))

    def get_current_node(self):
        """:rtype :TreeNode"""
        cur_index = self.__tree_view.currentIndex()
        """:type :QModelIndex"""
        return cur_index.internalPointer()

    def get_current_q_index(self):
        return self.__tree_view.currentIndex()

    def show_menu(self, point):
        selected_node = self.get_current_node()
        self.facade.sendNotification(Notes.SHOW_CONTEXT_MENU, ShowContextMenuVO(selected_node))

