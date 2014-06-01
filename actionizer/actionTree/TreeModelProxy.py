from actionTree.model.TreeManager import TreeManager
from notifications.notes import Notes, TreeNodeRenamedVO, TreeModelMovedVO, HotkeyChangedVO
from puremvc.patterns.facade import Facade
from puremvc.patterns.proxy import Proxy

__author__ = 'cfe'


class TreeModelProxy(Proxy):
    NAME = "TreeModelProxy"

    def __init__(self):
        super(TreeModelProxy, self).__init__(TreeModelProxy.NAME)
        self.__tree = TreeManager()
        self.setData(self.__tree)

    def add(self, child, *indexes):
        self.__tree.add(child, *indexes)
        self.sendNotification(
            Notes.TREE_MODEL_ADDED,
            {
                "child": child,
                "indexes": indexes,
                "root": self.__tree.root_node
            }
        )

    def remove(self, *i_indexes):
        removed_child = self.__tree.remove(*i_indexes)
        self.sendNotification(
            Notes.TREE_MODEL_REMOVED,
            {
                "indexes": i_indexes,
                "root": self.__tree.root_node,
                "child": removed_child,
            }
        )
        return removed_child

    def move(self, from_indexes, to_indexes):
        from_indexes, to_indexes = self.__tree.move(from_indexes, to_indexes)
        if from_indexes and to_indexes:
            self.facade.sendNotification(Notes.TREE_MODEL_MOVED, TreeModelMovedVO(from_indexes, to_indexes))

    def replace(self, new_node, *indexes):
        self.remove(*indexes)
        self.add(new_node, *indexes)

    def rename(self, new_name, *indexes):
        renamed_node = self.__tree.rename(new_name, *indexes)
        Facade.getInstance().sendNotification(
            Notes.TREE_NODE_RENAMED,
            TreeNodeRenamedVO(new_name, indexes),
        )

    def play(self, *indexes):
        self.__tree.play(*indexes)

    def get_type(self, *indexes):
        self.__tree.get_type(*indexes)

    def set_expanded(self, has_expanded, *indexes):
        self.__tree.set_expanded(has_expanded, *indexes)

    def set_hotkey(self, hotkey_str, *indexes):
        self.__tree.set_hotkey(hotkey_str, *indexes)
        self.facade.sendNotification(
            Notes.HOTKEY_CHANGED,
            HotkeyChangedVO(hotkey_str, indexes),
        )

    def get_indexes(self, tree_node):
        return self.__tree.get_indexes(tree_node)

    def save(self):
        self.__tree.save()
        self.sendNotification(Notes.TREE_MODEL_SAVED)

    def load(self):
        print("loading")
        self.__tree.load()
        self.sendNotification(Notes.TREE_MODEL_LOADED,
                              {"root": self.__tree.root_node})

    def __getitem__(self, i):
        return self.__tree[i]
