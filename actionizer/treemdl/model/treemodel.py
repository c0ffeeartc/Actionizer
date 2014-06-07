from PySide import QtCore
from PySide.QtCore import QAbstractItemModel, QModelIndex
from treemdl.model.treenode import TreeNode

__author__ = 'c0ffee'


class TreeModel (QAbstractItemModel):
    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeNode()
        self.rootItem.leaf = ["Name", "Type"]

    def get_root_index(self):
        return self.createIndex(self.rootItem)

    def __getitem__(self, i):
        return self.rootItem[i]

    # ------------------------------------------------------------
    # required overrides for QAbstractItemModel
    # ------------------------------------------------------------
    # When subclassing PySide.QtCore.QAbstractItemModel , at the very least you must implement
    # PySide.QtCore.QAbstractItemModel.index() ,
    # PySide.QtCore.QAbstractItemModel.parent() ,
    # PySide.QtCore.QAbstractItemModel.rowCount() ,
    # PySide.QtCore.QAbstractItemModel.columnCount() ,
    # and PySide.QtCore.QAbstractItemModel.data()
    # These functions are used in all read-only models, and form the basis of editable models.

    def index(self, i, column, parent_index):
        """
        :param i: in parent table
        :param column: in parent table
        :type parent_index: QModelIndex
        :rtype :QModelIndex
        """
        if not self.hasIndex(i, column, parent_index):
            return QModelIndex()

        if not parent_index.isValid():
                parent_node = self.rootItem
        else:
            parent_node = parent_index.internalPointer()

        child_node = parent_node[i]
        if child_node is not None:
            return self.createIndex(i, column, child_node)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_node = index.internalPointer()
        """:type :TreeNode"""
        parent_node = child_node.parent_node
        """:type :TreeNode"""

        if parent_node is None:
            return QtCore.QModelIndex()

        return self.createIndex(parent_node.get_index(), 0, parent_node)

    def rowCount(self, parent_index):
        if parent_index.column() > 0:
            return 0

        if not parent_index.isValid():
            parent_node = self.rootItem
        else:
            parent_node = parent_index.internalPointer()

        return len(parent_node)

    def columnCount(self, parent_index):
        if parent_index.isValid():
            return parent_index.internalPointer().get_column_count()
        else:
            return self.rootItem.get_column_count()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        node = index.internalPointer()

        return node.get_column_data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.get_column_data(section)

        return None
