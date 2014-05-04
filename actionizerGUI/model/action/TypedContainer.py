__author__ = 'cfe'


class TypedContainer(object):
    """
    List wrapper that can add and remove step_items of particular type specified in type_names
    """
    NAME = "TypedContainer"

    def __init__(self, type_name=None):
        self.items = []
        self.type_names = []
        if type_name:
            self.type_names.append(type_name)

    def clear(self):
        del self.items[:]

    def __getitem__(self, i):
        return self.items[i]

    def reinit(self, items):
        self.clear()
        for item in items:
            self.insert(item)

    def insert(self, item, i=None):
        if type(item) in self.type_names:
            # fix i
            len_items = len(self.items)
            if not i or i > len_items:
                i = len_items
            elif i < 0:
                i = 0
            # insert item
            self.items.insert(i, item)

    def pop(self, i):
        if len(self.items) > i >= 0:
            return self.items.pop(i)

    def jsonify(self):
        return {
            "__class__": TypedContainer.NAME,
            "__value__":
            {
                "step_items": self.items,
                "type_names": self.type_names,
            }
        }

    @classmethod
    def dejsonify(cls, o):
        if o['__class__'] == TypedContainer.NAME:
            cont = TypedContainer()
            cont.type_names = o["__value__"]["type_names"]
            cont.items = o["__value__"]["step_items"]
            return cont
