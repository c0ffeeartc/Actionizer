from PySide import QtGui
from PySide.QtGui import QTreeWidgetItem
from actionTree.TreeModelProxy import TreeModelProxy
from actionTree.model.ActionGroup import ActionGroup
from options.OptionsVO import Options
from treeView.view.TreeView import TreeView
from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator

__author__ = 'cfe'


class TreeViewMediator(Mediator):
    NAME = "TreeViewMediator"

    def __init__(self):
        super(TreeViewMediator, self).__init__(TreeViewMediator.NAME, TreeView())
        self.__tree_view = self.viewComponent
        """:type :TreeView"""

    def listNotificationInterests(self):
        return [
            Notes.TREE_NODE_RENAMED,
            Notes.TREE_MODEL_CHANGED,
            Notes.TREE_MODEL_SAVE,
            Notes.TREE_MODEL_LOAD,
            Notes.TREE_MODEL_SAVED,
            Notes.TREE_MODEL_LOADED,
            Notes.TREE_MODEL_ADD,
            Notes.TREE_MODEL_ADDED,
            Notes.TREE_MODEL_REMOVE,
            Notes.TREE_MODEL_REMOVED,
        ]

    def handleNotification(self, note):
        tree_model_proxy = self.facade.retrieveProxy(TreeModelProxy.NAME)
        """:type :TreeModelProxy"""
        if note.name == Notes.TREE_MODEL_SAVE:
            tree_model_proxy.save()
        elif note.name == Notes.TREE_MODEL_LOAD:
            tree_model_proxy.load()
        elif note.name == Notes.TREE_MODEL_SAVED:
            print("saved")
        elif note.name == Notes.TREE_MODEL_LOADED:
            print("updating on loaded")
            self.__tree_view.clear()
            self.__tree_view.update(note.body["root"])
        elif note.name == Notes.TREE_NODE_RENAMED:
            self.get_cur_item().setText(0, note.body["new_name"])
        elif note.name == Notes.TREE_MODEL_ADDED:
            indexes = note.body["indexes"]
            child_node = note.body["child"]
            """:type :actionTree.model.TreeNode.TreeNode"""
            child = QTreeWidgetItem(
                None,
                [child_node.leaf.name, child_node.leaf.NAME]
            )
            self.__tree_view.add(child, *indexes)
            if child.text(1) == ActionGroup.NAME:
                child.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                child.setIcon(0, QtGui.QIcon(
                    Options.assets_path + "folder_16x16.png"))
        elif note.name == Notes.TREE_MODEL_REMOVE:
            cur = self.get_cur_item()
            indexes = self.__tree_view.get_indexes(cur)
            tree_model_proxy.remove(*indexes)
        elif note.name == Notes.TREE_MODEL_REMOVED:
            indexes = note.body["indexes"]
            """:type :list"""
            self.__tree_view.remove(*indexes)

    def get_indexes(self, tree_item):
        """:rtype :list of int"""
        return self.__tree_view.get_indexes(tree_item)

    def get_cur_item(self):
        """:rtype :PySide.QtGui.QTreeWidgetItem.QTreeWidgetItem"""
        return self.__tree_view.currentItem()

    # replaces step
    # step_uid = note.body["txt"]
    # tree = self.get_main_window().tree
    # old_item = tree.currentItem()
    # item_parent = old_item.parent()
    # old_item_index = old_item.parent().indexOfChild(old_item)
    # item_parent.removeChild(old_item)
    # self.get_main_window().add_step(step_uid, item_parent,
    # old_item_index)
