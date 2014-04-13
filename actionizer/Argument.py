__author__ = 'cfe'


class Argument(object):
    """
    Argument is an overhead for [value, name] list
    and its probable changes in future
    """
    def __init__(self):
        self.__make_empty()

    def __make_empty(self):
        self.value = None
        self.name = None
        self.type_name = None

    def from_list(self, argumentAsList):
        if argumentAsList:
            self.value = argumentAsList[0]
            self.type_name = argumentAsList[1]
            self.name = argumentAsList[2]

    def to_list(self):
        return [
            self.value,
            self.type_name,
            self.name,
        ]
