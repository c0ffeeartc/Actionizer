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

    def update(self, action_root, *indexes):
        self.clear()
        print("update")
        for action_group in action_root.children:
            print(action_group)
            for action in action_group.children:
                print(action)
                for step in action.children:
                    print(step)
