from PySide import QtGui
from PySide.QtCore import Qt
from PySide.QtGui import QTreeWidget, QTreeWidgetItem

from actionTree.model.UI import UI
from notifications.notes import Notes, ShowContextMenuVO
from options.OptionsVO import Options
from puremvc.patterns.facade import Facade


__author__ = 'c0ffee'


class TreeView(QTreeWidget):
    def __init__(self):
        super(TreeView, self).__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.customContextMenuRequested.connect(self.show_menu)

        self.setHeaderItem(QTreeWidgetItem(None, ["Name", "TYPE_NAME"]))
        self.setColumnCount(3)
        self.setColumnWidth(0, 300)

    def show_menu(self, point):
        selected_item = self.itemAt(point)
        Facade.getInstance().sendNotification(Notes.SHOW_CONTEXT_MENU, ShowContextMenuVO(self, selected_item))

    def update(self, parent_node):
        """
        Recursively updates treeView item branch
        :type parent_node: actionTree.model.TreeNode.TreeNode
        """
        for child_node in parent_node.children:
            i_parent = parent_node.get_indexes()
            item = self.__make_item(child_node.leaf.name, child_node.leaf.NAME)
            self.__get_target(*i_parent).addChild(item)
            if len(child_node.children):
                self.update(child_node)

    def __get_target(self, *indexes):
        """
        :rtype :QTreeWidgetItem
        """
        target = self.invisibleRootItem()
        for i in indexes:
            target = target.child(i)
        return target

    def get_indexes(self, tree_item):
        """
        :type tree_item:QTreeWidgetItem
        :rtype :list of int
        """
        indexes = []
        parent = tree_item.parent()
        """:type :QTreeWidgetItem"""
        while parent:
            indexes.insert(0, parent.indexOfChild(tree_item))
            tree_item = parent
            parent = tree_item.parent()
        i_at_root = self.invisibleRootItem().indexOfChild(tree_item)
        indexes.insert(0, i_at_root)
        return indexes

    def add(self, child, *indexes):
        """
        :type :QTreeWidgetItem
        """
        i_parent = indexes[:-1]
        i_target = indexes[-1]
        self.__get_target(*i_parent).insertChild(i_target, child)

    def remove(self, *indexes):
        i_parent = indexes[:-1]
        i_target = indexes[-1]
        self.__get_target(*i_parent).takeChild(i_target)

    def __make_item(self, name, type_name):
        item = QTreeWidgetItem(None, [name, type_name])
        if type_name == UI.ACTION_GROUP:
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            item.setIcon(
                0, QtGui.QIcon(Options.assets_path + "folder_16x16.png"))
        return item
