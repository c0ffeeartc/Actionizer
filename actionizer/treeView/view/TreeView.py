from PySide.QtCore import Qt
from PySide.QtGui import QTreeWidget, QTreeWidgetItem, QCursor

from actionTree.model.UI import UI
from contextMenu.StepContextMenu import StepContextMenu

__author__ = 'c0ffee'


# TODO: create mediator and sync with actionRoot
class TreeView(QTreeWidget):
    def __init__(self):
        super(TreeView, self).__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.setHeaderItem(QTreeWidgetItem(None, ["Name", "TYPE_NAME"]))
        self.setColumnCount(3)

    def show_menu(self, point):
        tree_item = self.itemAt(point)
        if tree_item and tree_item.text(1) == UI.STEP:
            StepContextMenu(self).popup(QCursor().pos())

    def update(self, parent_node, *indexes):
        """
        Recursively updates treeView item branch
        """
        print("update")
        for child_node in parent_node.children:
            i_parent = parent_node.get_indexes()
            item = self.__make_item(child_node.leaf.name, child_node.leaf.NAME)
            self.__get_target(*i_parent).addChild(item)
            if len(child_node.children):
                self.update(child_node)

    def __get_target(self, *indexes):
        target = self.invisibleRootItem()
        for i in indexes:
            target = target.child(i)
        return target

    def __make_item(self, name, type_name):
        item = QTreeWidgetItem(None, [name, type_name])
        if type_name == UI.ACTION_GROUP:
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            # item.setIcon(
            #     0, QtGui.QIcon(Options.assets_path + "folder_16x16.png"))
        return item
