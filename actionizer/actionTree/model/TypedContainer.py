__author__ = 'cfe'


class TypedContainer(object):
    """
    List wrapper that can insert, pop and clear children of particular type specified in type_names
    """
    NAME = "TypedContainer"

    def __init__(self, type_name=None):
        self.__children = []
        self.type_names = []
        if type_name:
            self.type_names.append(type_name)

    def add(self, child, i=None):
        """
        Insert child within container bounds
        """
        if child.type_name in self.type_names:
            # fix i
            len_items = len(self.__children)
            if i is None or i > len_items:
                i = len_items
            elif i < 0:
                i = 0
            # insert child
            self.__children.insert(i, child)

    def remove(self, i):
        """
        Pop child for valid i
        """
        if len(self.__children) > i >= 0:
            return self.__children.pop(i)

    def clear(self):
        del self.__children[:]

    def move(self, from_i, to_i):
        if to_i < len(self.__children) and from_i <= len(self.__children):
            self.__children.insert(to_i, self.__children.pop(from_i))

    def move_up(self, i):
        last = len(self.__children) - 1
        if last >= i > 0:
            self.move(i, i - 1)

    def move_down(self, i):
        last = len(self.__children) - 1
        if last > i >= 0:
            self.move(i, i + 1)

    def __getitem__(self, i):
        return self.__children[i]

    def jsonify(self):
        return {
            "__class__": TypedContainer.NAME,
            "__value__":
            {
                "children": self.__children,
                "type_names": self.type_names,
            }
        }

    @classmethod
    def dejsonify(cls, o):
        if o['__class__'] == TypedContainer.NAME:
            cont = TypedContainer()
            cont.type_names = o["__value__"]["type_names"]
            cont.__children = o["__value__"]["children"]
            return cont
