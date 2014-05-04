from PySide.QtCore import Qt
from PySide.QtGui import QTreeWidget, QTreeWidgetItem, QCursor
from model.UI import UI
from view.contextMenu.StepContextMenu import StepContextMenu

__author__ = 'c0ffee'


# TODO: create mediator and sync with actionRoot
class ActionTree(QTreeWidget):
    def __init__(self):
        super(ActionTree, self).__init__()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self.setHeaderItem(QTreeWidgetItem(None, ["Name", "TYPE_NAME"]))
        self.setColumnCount(3)

    def show_menu(self, point):
        tree_item = self.itemAt(point)
        if tree_item and tree_item.text(1) == UI.STEP:
            StepContextMenu(self).popup(QCursor().pos())
