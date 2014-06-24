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
