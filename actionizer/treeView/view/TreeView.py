from PySide import QtGui, QtCore
from PySide.QtCore import Qt, QEvent
from PySide.QtGui import QTreeWidget, QTreeWidgetItem, QAbstractItemView

from actionTree.model.UI import UI
from notifications.notes import Notes, ShowContextMenuVO, TreeModelMoveVO
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

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.installEventFilter(self)

        self.__drag_item = "None"
        self.dragSignal = QtCore.Signal(dict)

    def show_menu(self, point):
        selected_item = self.itemAt(point)
        Facade.getInstance().sendNotification(Notes.SHOW_CONTEXT_MENU, ShowContextMenuVO(self, selected_item))

    def eventFilter(self, source, event):
        # print(event.type())
        if event.type() == QEvent.Drop:
            print("filter drop")
            return True
        if event.type() == QEvent.ChildAdded and source is self:
            print("filter added")
            return True
        if event.type() == QEvent.ChildRemoved and source is self:
            print("filter removed")
            return True
        return QtGui.QTreeWidget.eventFilter(self, source, event)

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

    def move_item(self, from_indexes, to_indexes):
        child = self.remove(*from_indexes)
        self.add(child, *to_indexes)

    def mousePressEvent(self, e):
        """:type e: QMouseEvent.QMouseEvent"""
        pressed_item = self.itemAt(e.pos())
        if pressed_item:
            self.__drag_item = pressed_item
        QTreeWidget.mousePressEvent(self, e)

    def mouseMoveEvent(self, e):
        pass

    def mouseReleaseEvent(self, e):
        """:type e: QMouseEvent.QMouseEvent"""
        if self.__drag_item:
            released_item = self.itemAt(e.pos())
            if released_item and released_item is not self.__drag_item:
                drag_indexes = self.get_indexes(self.__drag_item)
                released_indexes = self.get_indexes(released_item)
                Facade.getInstance().sendNotification(Notes.TREE_MODEL_MOVE, TreeModelMoveVO(drag_indexes, released_indexes))
        QTreeWidget.mouseReleaseEvent(self, e)
        self.__drag_item = None

    def get_type(self, item):
        return item.text(1)

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
        return self.__get_target(*i_parent).takeChild(i_target)

    def __make_item(self, name, type_name):
        item = QTreeWidgetItem(None, [name, type_name])
        if type_name == UI.ACTION_GROUP:
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            item.setIcon(
                0, QtGui.QIcon(Options.assets_path + "folder_16x16.png"))
        return item
