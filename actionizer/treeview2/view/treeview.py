from PySide.QtCore import Qt
from PySide.QtGui import QTreeView, QAbstractItemView

__author__ = 'c0ffee'


class TreeView(QTreeView):
    def __init__(self, model, *args, **kwargs):
        super(TreeView, self).__init__(*args, **kwargs)
        self.setModel(model)
        self.setColumnWidth(0, 200)
        self.setIndentation(15)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def startDrag(self, supportedActions):
        selected_indexes = self.selectedIndexes()
        selection = [q_index for q_index in selected_indexes if q_index.column() == 0]
        self.model().drag_q_indexes = selection
        super(TreeView, self).startDrag(supportedActions)
