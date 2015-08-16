from PySide import QtCore
from PySide.QtCore import QAbstractItemModel, QModelIndex

from treedataleaf.ActionRoot import ActionRoot
from treemdl.model.treenode import TreeNode


__author__ = 'c0ffee'


class TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        """
        :type parent: PySide.QtCore.QObject
        """
        super(TreeModel, self).__init__(parent)
        self.root_node = TreeNode(ActionRoot())
        # TODO: allow dragging more than one item
        self.drag_q_indexes = None
        """:type :list of QModelIndex"""
        self.target_q_index = None
        """:type :QModelIndex"""
        self.target_node = None
        """:type :TreeNode"""
        self.target_i = None

    def get_root_index(self):
        return self.createIndex(self.root_node)

    def __getitem__(self, i):
        return self.root_node[i]

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
        :param i: row in parent table
        :param column: in parent table
        :type parent_index: QModelIndex
        :rtype :QModelIndex
        """
        if not self.hasIndex(i, column, parent_index):
            return QModelIndex()

        if not parent_index.isValid():
            parent_node = self.root_node
        else:
            parent_node = parent_index.internalPointer()

        child_node = parent_node[i]
        if child_node is not None:
            return self.createIndex(i, column, child_node)
        else:
            return QModelIndex()

    def parent(self, index):
        """
        :type index: QModelIndex
        :rtype :QModelIndex
        """
        if not index.isValid():
            return QtCore.QModelIndex()

        child_node = index.internalPointer()
        """:type :TreeNode"""
        parent_node = child_node.parent_node
        """:type :TreeNode"""

        if not parent_node:
            return QtCore.QModelIndex()

        return self.createIndex(parent_node.get_row(), 0, parent_node)

    def rowCount(self, parent_index):
        if parent_index.column() > 0:
            return 0

        if not parent_index.isValid():
            parent_node = self.root_node
        else:
            parent_node = parent_index.internalPointer()

        return len(parent_node.child_nodes)

    def columnCount(self, parent_index):
        if parent_index.isValid():
            return parent_index.internalPointer().get_column_count()
        else:
            return self.root_node.get_column_count()

    def data(self, index, role):
        """
        @type index: QModelIndex
        @param role:
        @return:
        """
        if not index.isValid():
            return None

        if not role == QtCore.Qt.DisplayRole:
            return None

        node = index.internalPointer()

        return node.get_column_data(index.column())

    def dropMimeData(self, data, action, row, column, parent):
        """
        :type data:QMimeData
        :type action:DropAction
        :type row:QtCore.int
        :type column:QtCore.int
        :type parent:QModelIndex
        :rtype :QtCore.bool
        """
        parent_node = parent.internalPointer()
        """:type :TreeNode"""
        self.target_q_index = parent
        self.target_node = parent_node
        drag_node = self.drag_q_indexes[0].internalPointer()
        if row == -1:
            self.target_i = 0
        else:
            if drag_node.parent_node is parent_node and\
                    drag_node.get_row() < row:
                row -= 1
            self.target_i = row
        return bool(self.target_node)

    def supportedDropActions(self, *args, **kwargs):
        return QtCore.Qt.MoveAction

    def removeRows(self, row, count, parent):
        """
        :type row: QtCore.int
        :type count: QtCore.int
        :type parent: QModelIndex
        :rtype :PySide.QtCore.bool
        """
        if self.target_node is not None and self.target_i is not None:
            if not self.beginMoveRows(parent, row, row + count-1, self.target_q_index, self.target_i):
                return False
            parent_node = parent.internalPointer()
            """:type :TreeNode"""
            node_to_move = parent_node[row]
            """:type :TreeNode"""
            is_move_allowed = self.target_node.is_allowed_child(node_to_move.get_type())
            if not is_move_allowed:
                self.target_q_index = None
                self.target_node = None
                self.target_i = None
                return False
            node_to_move = parent_node.remove(row)
            self.target_node.add(node_to_move, self.target_i)
            self.endMoveRows()

            self.target_q_index = None
            self.target_node = None
            self.target_i = None
            return True
        else:
            self.target_q_index = None
            self.target_node = None
            self.target_i = None
            return False

    def insertRows(self, *args, **kwargs):
        super(TreeModel, self).insertRows(self, *args, **kwargs)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        @type index:QModelIndex
        @param value: object
        @param role: PySide.QtCore.int
        @return:
        """
        # TODO: don't accept rename on click outside of edit field
        if value == "":
            return False
        cur_node = index.internalPointer()
        cur_node.rename(value)
        return True

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        if index.column() != 0:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | \
                QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable |\
                QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"
            if section == 1:
                return "Type"
        return None
