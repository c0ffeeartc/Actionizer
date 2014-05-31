from PySide.QtGui import QTreeWidgetItem
from actionTree.TreeModelProxy import TreeModelProxy
from treeView.view.TreeView import TreeView
from notifications.notes import Notes
from puremvc.patterns.mediator import Mediator

__author__ = 'cfe'


class TreeViewMediator(Mediator):
    NAME = "TreeViewMediator"

    def __init__(self):
        super(TreeViewMediator, self).__init__(TreeViewMediator.NAME, TreeView())
        self.__tree_view = self.viewComponent
        """:type :TreeView"""

    def listNotificationInterests(self):
        return [
            Notes.TREE_NODE_RENAMED,
            Notes.TREE_MODEL_CHANGED,
            Notes.TREE_MODEL_SAVE,
            Notes.TREE_MODEL_LOAD,
            Notes.TREE_MODEL_SAVED,
            Notes.TREE_MODEL_LOADED,
            Notes.TREE_MODEL_ADD,
            Notes.TREE_MODEL_ADDED,
            Notes.TREE_MODEL_REMOVE,
            Notes.TREE_MODEL_REMOVED,
            Notes.TREE_MODEL_MOVE,
            Notes.TREE_MODEL_MOVED,
            Notes.TREE_MODEL_EXPANDED,
        ]

    def handleNotification(self, note):
        tree_model_proxy = self.facade.retrieveProxy(TreeModelProxy.NAME)
        """:type :TreeModelProxy"""

        if note.name == Notes.TREE_MODEL_EXPANDED:
            vo = note.body
            """:type :TreeModelExpandedVO"""
            tree_model_proxy.set_expanded(vo.has_expanded, *vo.indexes)

        elif note.name == Notes.TREE_MODEL_SAVE:
            tree_model_proxy.save()

        elif note.name == Notes.TREE_MODEL_LOAD:
            tree_model_proxy.load()

        elif note.name == Notes.TREE_MODEL_SAVED:
            print("saved")

        elif note.name == Notes.TREE_MODEL_LOADED:
            print("updating on loaded")
            self.__tree_view.clear()
            self.__tree_view.update(note.body["root"])

        elif note.name == Notes.TREE_NODE_RENAMED:
            vo = note.body
            """:type :TreeNodeRenamedVO"""
            self.get_cur_item().setText(0, vo.new_name)

        elif note.name == Notes.TREE_MODEL_ADDED:
            indexes = note.body["indexes"]
            child_node = note.body["child"]
            """:type :actionTree.model.TreeNode.TreeNode"""
            child = QTreeWidgetItem(
                None,
                [child_node.leaf.name, child_node.leaf.NAME]
            )
            self.__tree_view.add(child, *indexes)

        elif note.name == Notes.TREE_MODEL_REMOVE:
            cur = self.get_cur_item()
            indexes = self.__tree_view.get_indexes(cur)
            tree_model_proxy.remove(*indexes)

        elif note.name == Notes.TREE_MODEL_REMOVED:
            indexes = note.body["indexes"]
            """:type :list"""
            self.__tree_view.remove(*indexes)

        elif note.name == Notes.TREE_MODEL_MOVE:
            vo = note.body
            """@type :TreeModelMoveVO"""
            tree_model_proxy.move(vo.drag_indexes, vo.target_indexes)

        elif note.name == Notes.TREE_MODEL_MOVED:
            vo = note.body
            """@type :TreeModelMovedVO"""
            self.__tree_view.move_item(vo.drag_indexes, vo.target_indexes)

    def get_indexes(self, tree_item):
        """:rtype :list of int"""
        return self.__tree_view.get_indexes(tree_item)

    def get_cur_item(self):
        """:rtype :PySide.QtGui.QTreeWidgetItem.QTreeWidgetItem"""
        return self.__tree_view.currentItem()

    def get_type_name(self, q_tree_item):
        """:type q_tree_item:PySide.QtGui.QTreeWidgetItem.QTreeWidgetItem"""
        return q_tree_item.text(1)
