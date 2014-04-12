from Argument import Argument

__author__ = 'cfe'


class Arguments(object):
    """
    Container for Argument objects, with helpful functionality for convertion to
    plain lists and psArguments
    """

    def __init__(self):
        self.__makeEmpty()

    def __makeEmpty(self):
        self.argObjs = []
        self.typename = "argumentsClass"

    def add(self, *argObjs):
        for argObj in argObjs:
            if argObj.typename == "number" or \
                            argObj.typename == "string" or \
                            argObj.typename == "bool":
                self.argObjs.append(argObj)

    def fromList(self, argPlainList):
        self.argObjs = [Argument().fromList(arg) for arg in argPlainList]

    def asList(self):
        if self.argObjs:
            return [argObj.asList() for argObj in self.argObjs]
        else:
            return []

    def asPsArguments(self):
        psArguments = [len(self.args)]
        psArguments.extend([arg.asList() for arg in self.args])
        return psArguments
