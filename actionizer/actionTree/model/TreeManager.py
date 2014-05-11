from actionTree.model.ActionRoot import ActionRoot

__author__ = 'cfe'


class TreeManager(object):
    """
    Provides unified interface for tree nodes
    """
    def __init__(self):
        self.action_root = ActionRoot()

    def play(self, *indexes):
        self.__get_target(*indexes).play()

    def add(self, child, *indexes):
        i_path = indexes[0:-1]
        i_target = indexes[-1]
        self.__get_target(*i_path).add(child, i_target)

    def remove(self, *indexes):
        i_path = indexes[0:-1]
        i_target = indexes[-1]
        return self.__get_target(*i_path).pop(i_target)

    def save(self):
        self.action_root.save()

    def load(self):
        self.action_root.load()

    def __getitem__(self, i):
        return self.action_root[i]

    def __get_target(self, *indexes):
        target = self.action_root
        for i in indexes:
            target = target[i]
        return target
