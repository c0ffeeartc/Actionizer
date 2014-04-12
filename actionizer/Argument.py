__author__ = 'cfe'


class Argument(object):
    # Argument is an overhead for [value, typename, name] list
    # and its probable changes in future

    def __init__(self):
        self.__makeEmpty()

    def __makeEmpty(self):
        self.value = None
        self.name = None
        self.typename = None

    def fromList(self, argumentAsList):
        self.value = argumentAsList[0]
        self.typename = argumentAsList[1]
        self.name = argumentAsList[2]

    def asList(self):
        return [
            self.value,
            self.typename,
            self.name,
        ]
