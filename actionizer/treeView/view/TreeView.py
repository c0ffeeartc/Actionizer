from PySide import QtGui
from PySide.QtCore import Qt, QEvent
from PySide.QtGui import QTreeWidget, QTreeWidgetItem, QAbstractItemView
from actionTree.model.Action import Action
from actionTree.model.ActionGroup import ActionGroup
from actionTree.model.StepItem import StepItem

from actionTree.model.UI import UI
from notifications.notes import Notes, ShowContextMenuVO, TreeModelMoveVO, TreeModelExpandedVO
from options.OptionsVO import Options
from puremvc.patterns.facade import Facade


__author__ = 'c0ffee'


class TreeView(QTreeWidget):
    ACTION = Action.NAME
    ACTION_GROUP = ActionGroup.NAME
    STEP = StepItem.NAME

    def __init__(self):
        super(TreeView, self).__init__()
        self.setIndentation(10)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.customContextMenuRequested.connect(self.show_menu)

        self.setHeaderItem(QTreeWidgetItem(None, ["Name", "TYPE_NAME"]))
        self.setColumnCount(3)
        self.setColumnWidth(0, 200)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.installEventFilter(self)

        self.__drag_item = "None"

        # noinspection PyUnresolvedReferences
        self.itemExpanded.connect(self.on_item_expanded)
        # noinspection PyUnresolvedReferences
        self.itemCollapsed.connect(self.on_item_collapsed)

    def show_menu(self, point):
        selected_item = self.itemAt(point)
        Facade.getInstance().sendNotification(Notes.SHOW_CONTEXT_MENU, ShowContextMenuVO(self, selected_item))

    def eventFilter(self, source, event):
        # print(event.type())
        if event.type() == QEvent.Drop:
            print("filter drop")
            return True
        elif event.type() == QEvent.WindowActivate:
            Facade.instance.sendNotification(Notes.STOP_LISTEN_GLOBAL_HOTKEYS)
        elif event.type() == QEvent.WindowDeactivate:
            Facade.instance.sendNotification(Notes.START_LISTEN_GLOBAL_HOTKEYS)
        elif event.type() == QEvent.ChildAdded and source is self:
            print("filter added")
            return True
        elif event.type() == QEvent.ChildRemoved and source is self:
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
            parent_item = self.__get_target(*i_parent)
            """@type :QTreeWidgetItem"""
            indexes = []
            indexes.extend(i_parent)
            indexes.append(parent_item.childCount())
            item = self.__make_item(child_node.leaf.name, child_node.leaf.NAME)
            if child_node.leaf.NAME == UI.ACTION:
                item.setText(2, child_node.leaf.hotkey)
            self.add(item, *indexes)
            item.setExpanded(child_node.is_expanded)
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            if len(child_node.children):
                self.update(child_node)

    def set_hotkey(self, hotkey_str, *indexes):
        cur_item = self.__get_target(*indexes)
        if self.get_type(cur_item) == UI.ACTION:
            cur_item.setText(2, hotkey_str)

    def move_item(self, from_indexes, to_indexes):
        child = self.remove(*from_indexes)
        self.add(child, *to_indexes)
        self.setCurrentItem(child)

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
        child.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        if child.text(1) == ActionGroup.NAME:
            child.setIcon(0, QtGui.QIcon(
                Options.assets_path + "folder_16x16.png"))

    def remove(self, *indexes):
        i_parent = indexes[:-1]
        i_target = indexes[-1]
        return self.__get_target(*i_parent).takeChild(i_target)

    def __make_item(self, name, type_name):
        item = QTreeWidgetItem(None, [name, type_name])
        item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        if type_name == UI.ACTION_GROUP:
            item.setIcon(
                0, QtGui.QIcon(Options.assets_path + "folder_16x16.png"))
        return item

    def on_item_expanded(self, item):
        Facade.instance.sendNotification(Notes.TREE_MODEL_EXPANDED, TreeModelExpandedVO(True, self.get_indexes(item)))

    def on_item_collapsed(self, item):
        Facade.instance.sendNotification(Notes.TREE_MODEL_EXPANDED, TreeModelExpandedVO(False, self.get_indexes(item)))
